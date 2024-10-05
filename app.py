import os
from flask import Flask, request, redirect, url_for, flash, render_template, send_from_directory
from werkzeug.utils import secure_filename
from MachineLearningPredictions.Emotion_Detection import detect_emotion
from MachineLearningPredictions.Speech_Detection import detect_wav
from api_handler import get_feedback
import cv2 as cv
from audio_extract import extract_audio
import subprocess


# Starts the app
app = Flask(__name__)

emotions_list = []


@app.route("/")
def home():
    return render_template('index.html')

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
    print(emotion)
    emotions_list.append(emotion)
    return "Finished", 200


# Runs a single ffmpeg command to convert a video format to audio only
def convert_video_to_audio(video_file_path, audio_file_path):
    command = f"ffmpeg -y -i {video_file_path} -vn -af asetpts=N/SR/TB {audio_file_path}" 
    subprocess.call(command, shell=True)

# Get audio
@app.route('/upload_audio', methods=['POST'])
def upload_audio():
    audio = None
    print("Attempt upload")
    if 'audio_file' not in request.files:
        return "No audio in the request", 400
    
    # Delete both temporary audio files if they exist (for safety)
    if(os.path.exists(os.path.join(app.config['UPLOAD_FOLDER'], 'audio.webm'))):
        print("\n\n\nDELETE!!!!!!! ",os.path.join(app.config['UPLOAD_FOLDER'], 'audio.webm'),"\n\n\n")
        os.remove(os.path.join(app.config['UPLOAD_FOLDER'], 'audio.webm'))

    if(os.path.exists(os.path.join(app.config['UPLOAD_FOLDER'], 'audio.wav'))):
        print("\n\n\nDELETE!!!!!!! ",os.path.join(app.config['UPLOAD_FOLDER'], 'audio.wav'),"\n\n\n")
        os.remove(os.path.join(app.config['UPLOAD_FOLDER'], 'audio.wav'))
    
    # Wipe both files (if they still exist...)
    open(os.path.join(app.config['UPLOAD_FOLDER'], 'audio.webm'),'w').close() 
    open(os.path.join(app.config['UPLOAD_FOLDER'], 'audio.wav'),'w').close()
    audio = request.files['audio_file']

    # If no audio was sent, do nothing.
    if not audio:
        return "Failed to upload audio", 400

    audio_name = secure_filename(audio.filename) # Just for safety

    file_path = os.path.join(app.config['UPLOAD_FOLDER'], audio_name)
    audio.save(file_path) # Saves the audio to ./recordedFiles/audio.webm

    # New home path for the .wav file
    audio_file = os.path.join(app.config['UPLOAD_FOLDER'], 'audio.wav')
    convert_video_to_audio(file_path, audio_file) # Converts the .webm file to .wav format and saves it at ./recordedFiles/audio.wav
    

    # Now machine learning stuff
    # The wav file is sent to speech detection
    transcript = detect_wav(os.path.join(app.config['UPLOAD_FOLDER'], 'audio.wav'))
    print("Transcript is " + transcript)
    # The transcript from the speech detection is sent to groq to get feedback
    feedback = get_feedback(emotions_list, transcript)
    print("____________________ \n" + feedback)
    print("done ")
    return "Finished", 200


if __name__ == '__main__':
    app.run(debug=True)


