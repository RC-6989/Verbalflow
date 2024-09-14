const videoElement = document.getElementById('videoElement');
const canvasElement = document.getElementById('canvasElement');
const startButton = document.getElementById('startButton');
const stopButton = document.getElementById('stopButton');
const canvasContext = canvasElement.getContext('2d');

let stream;  // To store the media stream

// Function to start video capture
async function startVideoCapture() {
    try {
        stream = await navigator.mediaDevices.getUserMedia({ video: true });
        videoElement.srcObject = stream;
        startButton.disabled = true;
        stopButton.disabled = false;
        captureInterval = setInterval(sendFrameToBackend, 1000);
    } catch (err) {
        console.error("Error accessing the webcam:", err);
    }
}

// Function to stop video capture
function stopVideoCapture() {
    if (stream) {
        // Stop all video tracks in the stream
        stream.getTracks().forEach(track => track.stop());

        // Clear the video element
        videoElement.srcObject = null;

        // Re-enable the start button
        startButton.disabled = false;
        stopButton.disabled = true;
        clearInterval(captureInterval);
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
startButton.addEventListener('click', startVideoCapture);
stopButton.addEventListener('click', stopVideoCapture);

// Disable stop button initially
stopButton.disabled = true;