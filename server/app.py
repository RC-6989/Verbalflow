import os
from flask import Flask, request, redirect, url_for, flash, render_template, send_from_directory
from werkzeug.utils import secure_filename
import whisper

# Starts the app
app = Flask(__name__)

def talking(audioPath):
    model = whisper.load_model("base")
    result = model.transcribe(audioPath)
    return result["text"]


@app.route("/")
def home():
    return render_template('index.html')

# Basically app.use() in express
@app.route('/public/<path:path>')
def send_report(path):
    return send_from_directory('public', path)


# Route to handle image upload
@app.route('/upload', methods=['POST'])
def upload_image():
    # Secure the filename and save the file to the desired folder
    filename = secure_filename(file.filename)
    file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    file.save(file_path)
    return f"File uploaded successfully: {filename}"

UPLOAD_FOLDER = 'frames/'
app.config['UPLOAD_FOLDER'] = os.path.join(os.path.dirname(os.path.abspath(__file__)), UPLOAD_FOLDER)

# Get video
@app.route('/upload_frame', methods=['POST'])
def upload_frame():
    if 'frame' not in request.files:
        return "No frame part in the request", 400
    file = request.files['frame']
    if file:
        filename = secure_filename(file.filename)
        print("The file name is " + filename)
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(file_path)
        return "Frame received and saved", 200
    return "Failed to upload frame", 400

if __name__ == '__main__':
    app.run(debug=True)

