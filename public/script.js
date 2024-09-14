const videoElement = document.getElementById('videoElement');
const canvasElement = document.getElementById('canvasElement');
const startButton = document.getElementById('startButton');
const stopButton = document.getElementById('stopButton');
const canvasContext = canvasElement.getContext('2d');

let stream;  // To store the media stream
let mediaRecorder;
let recordedChunks = [];

// Function to start video capture
async function startRecording() {
    try {
        stream = await navigator.mediaDevices.getUserMedia({video: true, audio: true});
        videoElement.srcObject = stream;
        startButton.disabled = true;
        stopButton.disabled = false;
        captureInterval = setInterval(sendFrameToBackend, 1000);

        mediaRecorder = new MediaRecorder(stream);

        // Collect the audio data
        mediaRecorder.ondataavailable = function (event) {
            if (event.data.size > 0) {
                recordedChunks.push(event.data);
            }
        };

        // Stop recording
        mediaRecorder.onstop = async function () {
            const blob = new Blob(recordedChunks, { type: 'audio/wav' });
            const formData = new FormData();
            formData.append('audio_file', blob, 'audio.wav');

            // Send the audio blob to the Flask backend using fetch
            try {
                const response = await fetch('/upload_audio', {
                    method: 'POST',
                    body: formData
                });
            } catch (err) {
                console.error(err);
            }

            // Debug
            // const result = await response.json();
            // console.log('Server response:', result);
        };

        mediaRecorder.start();

    } catch (err) {
        console.error("Error accessing the webcam/microphone:", err);
    }
}

// Function to stop video capture
function stopRecording() {
    if (stream) {
        // Stop all video tracks in the stream
        stream.getTracks().forEach(track => track.stop());

        // Clear the video element
        videoElement.srcObject = null;

        // Re-enable the start button
        startButton.disabled = false;
        stopButton.disabled = true;
        clearInterval(captureInterval);

        mediaRecorder.stop();
    }
}

function sendFrameToBackend() {
    // Draw the current frame from the video onto the canvas
    canvasContext.drawImage(videoElement, 0, 0, canvasElement.width, canvasElement.height);

    // Convert the canvas content to a Blob (or base64 if needed)
    canvasElement.toBlob(async (blob) => {
        const formData = new FormData();
        formData.append('frame', blob, 'frame.png');

        try {
            // Send the image frame to the Flask backend via fetch
            await fetch('/upload_frame', {
                method: 'POST',
                body: formData
            });
            console.log('Frame sent to backend');
        } catch (err) {
            console.error('Error sending frame:', err);
        }
    }, 'image/png');
}

// Attach event listeners to the buttons
startButton.addEventListener('click', startRecording);
stopButton.addEventListener('click', stopRecording);

// Disable stop button initially
stopButton.disabled = true;