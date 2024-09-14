import os
from flask import Flask, request, redirect, url_for, flash, render_template, send_from_directory
from werkzeug.utils import secure_filename
import whisper
from MachineLearningPredictions.Emotion_Detection import detect_emotion


# Starts the app
app = Flask(__name__)

def talking(audioPath):
    model = whisper.load_model("base")
    result = model.transcribe(audioPath)
    return result["text"]


@app.route("/")
def home():
    return render_template('index.html', var1=emotion)

# Basically app.use() in express
@app.route('/public/<path:path>')
def send_report(path):
    return send_from_directory('public', path)

# Get video
@app.route('/upload_frame', methods=['POST'])
def upload_frame():
    if 'frame' not in request.files:
        return "No frame part in the request", 400
    file = request.files['frame']
    if file:
        emotion = detect_emotion(file)
        return "Frame received and saved", 200
    return "Failed to upload frame", 400

if __name__ == '__main__':
    app.run(debug=True)




