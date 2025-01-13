import os
import json
import threading
import subprocess
from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # Permitir CORS para todos los orígenes


@app.route('/check_subtitles', methods=['POST'])
def check_subtitles():
    data = request.json
    video_id = data.get('video_id')

    if not video_id:
        return jsonify({"error": "Video ID is required"}), 400

    # Verificar si existe el archivo de subtítulos
    file_path = os.path.join('subtitles_temp', f"{video_id}.json")
    if os.path.exists(file_path):
        return jsonify({"exists": True})  # Subtítulos encontrados
    else:
        return jsonify({"exists": False})  # Subtítulos no encontrados




@app.route('/get_subtitles', methods=['POST'])
def get_subtitles():
    print("Solicitud POST recibida")
    data = request.get_json()
    if not data:
        print("No se recibieron datos en la solicitud")
        return jsonify({"error": "No se recibieron datos"}), 400

    video_url = data.get('video_url')
    if not video_url:
        print("No se recibió la URL del video")
        return jsonify({"error": "No video URL provided"}), 400

    try:
        print(f"Descargando subtítulos para URL: {video_url}")
        subtitles = download_subtitles(video_url)

        # Crear el directorio si no existe
        os.makedirs("subtitles_temp", exist_ok=True)
        
        # Guardar los subtítulos como JSON
        video_id = video_url.split('v=')[1]
        json_file_path = os.path.join("subtitles_temp", f"{video_id}.json")
        with open(json_file_path, 'w', encoding='utf-8') as json_file:
            json.dump(subtitles, json_file, ensure_ascii=False, indent=4)

        print(f"Archivo JSON guardado en: {json_file_path}")
        return jsonify({"message": "Subtítulos procesados correctamente", "file_path": json_file_path})

    except Exception as e:
        print(f"Error procesando subtítulos: {str(e)}")
        return jsonify({"error": str(e)}), 500


def download_subtitles(video_url):
    # Extraer el video ID de la URL
    video_id = video_url.split('v=')[1]
    
    # Crear la carpeta donde se guardarán los subtítulos
    subtitulos_dir = "subtitles_temp"
    os.makedirs(subtitulos_dir, exist_ok=True)
    
    # Función para descargar los subtítulos subidos
    def download_uploaded_subs():
        comando_subidos = f'yt-dlp --write-subs --skip-download --sub-lang en --sub-format "vtt" --output "{subtitulos_dir}/{video_id}.subidos.%(ext)s" {video_url}'
        try:
            resultado_subidos = subprocess.run(comando_subidos, shell=True, check=True, capture_output=True, text=True)
            print(f"Subtítulos subidos descargados exitosamente: {resultado_subidos.stdout}")
        except subprocess.CalledProcessError as e:
            print(f"No se encontraron subtítulos subidos: {e.stderr}")

    # Función para descargar los subtítulos generados automáticamente
    def download_auto_subs():
        comando_auto_subs = f'yt-dlp --write-auto-subs --skip-download --sub-lang en --sub-format "vtt" --output "{subtitulos_dir}/{video_id}.auto.%(ext)s" {video_url}'
        try:
            resultado_auto_subs = subprocess.run(comando_auto_subs, shell=True, check=True, capture_output=True, text=True)
            print(f"Subtítulos generados automáticamente descargados: {resultado_auto_subs.stdout}")
        except subprocess.CalledProcessError as e:
            print(f"Error al descargar los subtítulos generados automáticamente: {e.stderr}")

    # Crear hilos para descargar ambos tipos de subtítulos en paralelo
    thread1 = threading.Thread(target=download_uploaded_subs)
    thread2 = threading.Thread(target=download_auto_subs)

    # Iniciar los hilos
    thread1.start()
    thread2.start()

    # Esperar que ambos hilos terminen
    thread1.join()
    thread2.join()

    # Verificar primero si existen los subtítulos subidos
    vtt_file_uploaded = os.path.join(subtitulos_dir, f"{video_id}.subidos.en.vtt")
    vtt_file_auto = os.path.join(subtitulos_dir, f"{video_id}.auto.en.vtt")

    if os.path.exists(vtt_file_uploaded):
        print("Usando subtítulos subidos.")
        return process_vtt_uploaded(vtt_file_uploaded)
    
    # Si no existen subtítulos subidos, usar los generados automáticamente
    elif os.path.exists(vtt_file_auto):
        print("Usando subtítulos generados automáticamente.")
        return process_vtt_auto(vtt_file_auto)

    # Si ninguno de los archivos existe
    raise RuntimeError("No se encontraron subtítulos disponibles (ni subidos ni generados automáticamente).")



def process_vtt_uploaded(vtt_file):
    # Procesar el archivo VTT y convertirlo a JSON estructurado
    subtitles = []
    with open(vtt_file, 'r', encoding='utf-8') as file:
        lines = file.readlines()
        
        current_caption = None
        for line in lines:
            line = line.strip()
            if "-->" in line:  # Identificar marca de tiempo
                start, end = line.split(" --> ")
                current_caption = {"start": start, "end": end, "text": ""}
            elif line:  # Acumular texto del subtítulo
                if current_caption:
                    current_caption["text"] += (" " + line).strip()
            else:  # Guardar subtítulo completo al encontrar una línea vacía
                if current_caption:
                    subtitles.append(current_caption)
                    current_caption = None

        # Agregar el último subtítulo si no está guardado
        if current_caption:
            subtitles.append(current_caption)

    print(f"Subtítulos procesados: {len(subtitles)}")
    return subtitles





def process_vtt_auto(vtt_file):
    # Procesar el archivo VTT de subtítulos generados automáticamente
    subtitles = []
    with open(vtt_file, 'r', encoding='utf-8') as file:
        lines = file.readlines()

        current_caption = None
        # Recorrer las líneas de abajo hacia arriba (comenzando desde la última línea)
        for i in range(len(lines) - 1, -1, -1):
            line = lines[i].strip()

            # Detener el proceso si la línea contiene "Kind: captions"
            if "Kind: captions" in line:
                break

            # Si encontramos un subtítulo (en líneas con índice %8 == 1)
            if i % 8 == 1:
                if current_caption and current_caption.get("text"):
                    subtitles.append(current_caption)  # Solo agregar el subtítulo si tiene texto
                current_caption = {"text": line}  # Almacenar el subtítulo

            # Si encontramos una marca de tiempo (en líneas con índice %8 == 4)
            elif i % 8 == 4:
                time_info = line.split(" --> ")
                if len(time_info) > 1:
                    start_time = time_info[0].strip()
                    end_time = time_info[1].split(" ")[0].strip()  # Limpiar cualquier dato adicional
                    if current_caption:
                        current_caption["start"] = start_time
                        current_caption["end"] = end_time

        # Agregar el último subtítulo si no está guardado
        if current_caption and current_caption.get("text"):
            subtitles.append(current_caption)

    # Los subtítulos se agregan en orden inverso, por lo que los revertimos
    subtitles.reverse()
    print(f"Subtítulos generados automáticamente procesados: {len(subtitles)}")
    return subtitles




@app.route('/subtitles_temp/<filename>')
def serve_subtitles(filename):
    return send_from_directory("subtitles_temp", filename)


if __name__ == '__main__':
    app.run(debug=True)











