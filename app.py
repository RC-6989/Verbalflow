import os
from flask import Flask, request, redirect, url_for, flash, render_template, send_from_directory
from werkzeug.utils import secure_filename
from MachineLearningPredictions.Emotion_Detection import detect_emotion
from MachineLearningPredictions.Speech_Detection import detect_wav
from api_handler import get_feedback
import cv2 as cv
from MachineLearningPredictions.Emotion_Detection import detect_emotion
# from MachineLearningPredictions.Speech_Detection import detect_wav

emotion = "NOTHING"
# Starts the app
app = Flask(__name__)

emotions_list = []


@app.route("/")
def home():
    return render_template('index.html', emo=emotion)

# Basically app.use() in express
@app.route('/public/<path:path>')
def send_report(path):
    return send_from_directory('public', path)


UPLOAD_FOLDER = 'recordedFiles/'
app.config['UPLOAD_FOLDER'] = os.path.join(os.path.dirname(os.path.abspath(__file__)), UPLOAD_FOLDER)

# Get video
@app.route('/upload_frame', methods=['POST'])
def upload_frame():
    if 'frame' not in request.files:
        return "No frame part in the request", 400
    file = request.files['frame']

    if not file:
        return "Failed to upload frame", 400

    filename = secure_filename(file.filename)
    file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    file.save(file_path)
    global emotion
    emotion = detect_emotion(file_path)

    return "Finished", 200

# Get audio
@app.route('/upload_audio', methods=['POST'])
def upload_audio():
    if 'audio_file' not in request.files:
        return "No audio in the request", 400
    audio = request.files['audio_file']

    print("Audio before:",type(audio))

    if not audio:
        return "Failed to upload audio", 400

    audio_name = secure_filename(audio.filename)

    print("Audio:",type(audio_name))

    file_path = os.path.join(app.config['UPLOAD_FOLDER'], audio_name)
    audio.save(file_path)
    # ADD STUFF HERE

    return "Finished", 200


if __name__ == '__main__':
    app.run(debug=True)



