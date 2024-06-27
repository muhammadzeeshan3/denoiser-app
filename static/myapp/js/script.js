/**
 * Handles the upload of audio files by the user.
 * This function is triggered when a user selects a file using the file input element.
 * It sends the file to the backend server to be processed, and then updates the UI.
 *
 * @param {HTMLInputElement} input - The input element that contains the file.
 */
function handleAudioUpload(input) {
    if (input.files && input.files[0]) {
        const formData = new FormData();
        formData.append("audio_file", input.files[0]);

        fetch('/api/denoiser/', {
            method: 'POST',
            headers: {
                'X-CSRFToken': csrfToken
            },
            body: formData
        })
        .then(response => response.json())
        .then(data => {
            updateUI(data);
            playOriginalAudio(data.original_path); // Play original audio after upload
        })
        .catch(error => {
            console.error('Error uploading or enhancing audio:', error);
        });
    }
}

/**
 * Updates the UI with the processed audio and graph images.
 *
 * @param {object} data - The response data from the backend server.
 */
function updateUI(data) {
    const originalAudio = document.getElementById('originalAudio');
    const enhancedAudio = document.getElementById('enhancedAudio');
    const originalGraph = document.getElementById('originalGraph');
    const enhancedGraph = document.getElementById('enhancedGraph');

    // Set original audio source
    originalAudio.src = `http://127.0.0.1:8000${data.Source_path}`;

    // Set enhanced audio source (if available)
    if (data.Target_path) {
        enhancedAudio.src = `http://127.0.0.1:8000${data.Target_path}`;
    } else {
        enhancedAudio.src = ''; // Handle if enhanced audio is not available
    }

    // Set background images for graphs
    originalGraph.style.backgroundImage = `url(http://127.0.0.1:8000${data.original_graph})`;
    enhancedGraph.style.backgroundImage = `url(http://127.0.0.1:8000${data.Target_graph})`;

    // Play original audio
    originalAudio.play();
}


