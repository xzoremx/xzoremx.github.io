// Espera a que el DOM esté completamente cargado antes de ejecutar el script
document.addEventListener("DOMContentLoaded", async () => {
    
    // Div para mostrar mensajes al usuario (estado, errores, etc.)
    const messageDiv = document.getElementById("message"); 
 
    // Contenedor de la animación de carga
    const loadingAnimation = document.getElementById("loading_animation");

    // Campo de entrada para el término de búsqueda
    const searchTermInput = document.getElementById("search-term");

    // Botón para iniciar la búsqueda
    const searchBtn = document.getElementById("search-btn");

    // Imagen del thumbnail del video
    const thumbnailImage = document.getElementById("thumbnail-image");



    //##################################################################################
    


    // Limpia cualquier mensaje previo que se haya mostrado al usuario
    messageDiv.innerHTML = "";

    // Oculta el campo de entrada de búsqueda, el botón y la imagen del thumbnail
    searchTermInput.style.display = "none";
    searchBtn.style.display = "none";
    thumbnailImage.style.display = "none";

    // Muestra la animación de carga mientras se realiza la búsqueda
    loadingAnimation.style.display = "block";




    //##################################################################################
    



    // Obtiene el ID del video de YouTube de la pestaña activa
    const videoId = await getYouTubeVideoId();
    
    // Si no se encuentra un video en la pestaña activa, muestra un mensaje de error después de un segundo
    if (!videoId) {
        setTimeout(() => {
            loadingAnimation.style.display = "none";
            showMessage("No YouTube video detected in the active tab.", "red");
        }, 1000);
        return;
    }



    //##################################################################################



    // Construye la URL del video y la URL del thumbnail usando el ID del video
    const videoUrl = `https://www.youtube.com/watch?v=${videoId}`;
    const thumbnailUrl = `https://img.youtube.com/vi/${videoId}/maxresdefault.jpg`;


    // Establece la imagen del thumbnail con la URL generada
    thumbnailImage.src = thumbnailUrl;

    // Ajusta el tamaño y estilo del thumbnail para que se muestre correctamente
    thumbnailImage.style.width = "100%";
    thumbnailImage.style.height = "auto";
    thumbnailImage.style.objectFit = "cover"; 
    thumbnailImage.style.borderRadius = "15px"; 



    //##################################################################################





    // Verificar si los subtítulos existen en el servidor para el video
    try {

        // Realiza una solicitud POST al servidor para comprobar si los subtítulos ya existen
        const checkResponse = await fetch('http://127.0.0.1:5000/check_subtitles', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json', 
            },
            body: JSON.stringify({ video_id: videoId }) // Envía el ID del video en el cuerpo de la solicitud
        });

        // Parsear la respuesta JSON del servidor
        const checkData = await checkResponse.json();

        // Si los subtítulos existen en el servidor, configura la UI y busca automáticamente si es necesario
        if (checkData.exists) {
            console.log("Subtitles already exist on the server.");

            // Oculta la animación de carga y muestra los elementos de la interfaz
            loadingAnimation.style.display = "none";        
            searchTermInput.style.display = "inline-block";
            searchBtn.style.display = "inline-block";
            thumbnailImage.style.display = "inline-block";

            
            // Verificar si hay un término de búsqueda previamente guardado en el almacenamiento local
            const lastSearchTerm = localStorage.getItem(`lastSearch_${videoId}`);
            if (lastSearchTerm) {
                searchTermInput.value = lastSearchTerm; // Prellenar el campo de búsqueda con el término guardado
                await performSearch(videoId, lastSearchTerm); // Ejecuta la búsqueda automáticamente usando el término guardado
            }

            return; // Termina la ejecución aquí si los subtítulos ya existen y todo está configurado
        }
        
    } catch (error) {
        console.error("Error checking subtitles on server:", error);
    }




    //##################################################################################




    // Si no existen subtítulos, se procede a generarlos
    try {
        
        // Realiza una solicitud POST al servidor para obtener o generar los subtítulos para el video
        const response = await fetch('http://127.0.0.1:5000/get_subtitles', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ video_url: videoUrl }) // Envía la URL del video en el cuerpo de la solicitud
        });



        // Verifica si la respuesta del servidor fue exitosa
        if (!response.ok) {
            throw new Error(`Error processing subtitles. Code: ${response.status}`);
        }
        


        // Parsear la respuesta JSON del servidor con los subtítulos procesados
        const data = await response.json();
        console.log("Subtitles processed correctly:", data);
        
        // Oculta la animación de carga y muestra un mensaje de éxito
        loadingAnimation.style.display = "none";
        showMessage("Subtitles found/generated successfully.", "white");




    } catch (error) {
        console.error("Error generating subtitles:", error);
        loadingAnimation.style.display = "none";
        showMessage("Subtitles could not be found or generated.", "red");
    }
});




//##################################################################################







// Función para mostrar un mensaje en la interfaz de usuario con un color determinado
function showMessage(message, color) {
    
    // Obtener los elementos necesarios de la interfaz
    const messageDiv = document.getElementById("message");
    const searchTermInput = document.getElementById("search-term");
    const searchBtn = document.getElementById("search-btn");
    const thumbnailImage = document.getElementById("thumbnail-image");

    // Mostrar el mensaje en el div de mensajes y establecer el color del texto
    messageDiv.innerHTML = message;
    messageDiv.style.color = color;

    // Personalización de la fuente y el estilo
    messageDiv.style.fontWeight = "bold";
    messageDiv.style.fontFamily = "'Arial', sans-serif"; 
    
    
    // Si el mensaje indica que los subtítulos fueron generados correctamente
    if (message === "Subtitles found/generated successfully.") {
        
        // Después de 3 segundos, limpiar el mensaje y mostrar los elementos ocultos 
        // (input de búsqueda, botón y thumbnail)
        setTimeout(() => {
            messageDiv.innerHTML = ""; 
            searchTermInput.style.display = "inline-block";
            searchBtn.style.display = "inline-block";
            thumbnailImage.style.display = "inline-block";
        }, 3000); 


        // Si el mensaje es de error (subtítulos no generados o no se detectó un video de YouTube) se cierra la extensión
    } else if (message === "Subtitles could not be found or generated." || 
               message === "No YouTube video detected in the active tab.") {
        setTimeout(() => {
            messageDiv.innerHTML = ""; 
            window.close();
        }, 3000); 
    }
}





//##################################################################################






// Función para convertir tiempo en formato hh:mm:ss.mmm a segundos
function convertTimeToSeconds(time) {
    const parts = time.split(':');
    const hours = parseInt(parts[0]) || 0;
    const minutes = parseInt(parts[1]) || 0;
    const seconds = parseFloat(parts[2]) || 0;
    return (hours * 3600) + (minutes * 60) + seconds;
}

// Función para convertir segundos a formato hh:mm:ss
function convertSecondsToTime(seconds) {
    const hrs = Math.floor(seconds / 3600);
    const mins = Math.floor((seconds % 3600) / 60);
    const secs = Math.floor(seconds % 60);
    return `${hrs.toString().padStart(2, '0')}:${mins.toString().padStart(2, '0')}:${secs.toString().padStart(2, '0')}`;
}







//##################################################################################






// Agrega un evento al botón de búsqueda que se ejecuta al hacer clic
document.getElementById("search-btn").addEventListener("click", async () => {
    
    
    // Obtiene el término de búsqueda y lo convierte a minúsculas
    const searchTerm = document.getElementById("search-term").value.toLowerCase();
    
    // Obtiene el ID del video de YouTube activo
    const videoId = await getYouTubeVideoId();


    // Si no se detecta un video de YouTube, muestra una alerta y termina la ejecución
    if (!videoId) {
        alert("No YouTube video detected in the active tab.");
        return;
    }

    // Llama a la función performSearch para realizar la búsqueda en los subtítulos
    await performSearch(videoId, searchTerm);
});






//##################################################################################






// Función para realizar la búsqueda en los subtítulos del video
async function performSearch(videoId, searchTerm) {
    
    // Obtiene el contenedor donde se mostrarán los resultados
    const resultsDiv = document.getElementById("results");
    resultsDiv.innerHTML = ""; // Limpia los resultados previos

    try {
        
        // Realiza una solicitud para obtener los subtítulos en formato JSON desde el servidor
        const response = await fetch(`http://127.0.0.1:5000/subtitles_temp/${videoId}.json`);


        // Si la respuesta del servidor no es exitosa, lanza un error
        if (!response.ok) {
            throw new Error(`Subtitle file not found for video ID: ${videoId}`);
        }


        // Parsear la respuesta JSON que contiene los subtítulos
        const subtitles = await response.json();
        console.log("Subtítulos cargados:", subtitles);


        // Filtra los subtítulos que contienen el término de búsqueda (sin distinguir mayúsculas/minúsculas)
        const results = subtitles.filter(sub => sub.text.toLowerCase().includes(searchTerm));



        // Si no se encuentran resultados, muestra un mensaje indicando que no se encontró nada
        if (results.length === 0) {
            resultsDiv.innerHTML = "<p>No results were found for the search term.</p>";
        } else {

            // Si se encuentran resultados, muestra cada uno con su timestamp correspondiente
            results.forEach(({ start, text }) => {
                let readableTimestamp = "00:00:00";
                if (start) {
                    try {
                        const seconds = convertTimeToSeconds(start);
                        readableTimestamp = convertSecondsToTime(seconds);
                    } catch (error) {
                        console.error("Error converting timestamp:", start, error);
                    }
                }

                // Crea un enlace para el timestamp que dirige al video en YouTube
                const timestampLink = document.createElement("a");
                timestampLink.href = `https://www.youtube.com/watch?v=${videoId}&t=${convertTimeToSeconds(start)}s`;
                timestampLink.target = "_blank";
                timestampLink.innerHTML = `<strong>${readableTimestamp}</strong>`;


                // Crea un div para el resultado y agrega el enlace y el texto del subtítulo
                const result = document.createElement("div");
                result.appendChild(timestampLink);
                result.innerHTML += `: ${text}`;


                // Agrega el resultado al contenedor de resultados
                resultsDiv.appendChild(result);
            });
            
            // Guarda el último término de búsqueda en el almacenamiento local para usarlo en futuras búsquedas
            localStorage.setItem(`lastSearch_${videoId}`, searchTerm);
        }



        
    } catch (error) {
        console.error("Search error:", error);
        alert("There was a problem searching for subtitles.");
    }
}




//##################################################################################





// Función para obtener el ID del video de YouTube
function getYouTubeVideoId() {
    return new Promise((resolve) => {
        chrome.tabs.query({ active: true, currentWindow: true }, function (tabs) {
            const url = tabs[0].url;
            const videoIdMatch = url.match(/[?&]v=([a-zA-Z0-9_-]+)/);
            resolve(videoIdMatch ? videoIdMatch[1] : null);
        });
    });
}




//##################################################################################







