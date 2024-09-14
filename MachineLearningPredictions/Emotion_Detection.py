#importing dependencies
import cv2 as cv
from deepface import DeepFace
import numpy as np

models = [
  "VGG-Face",
  "Facenet",
  "Facenet512",
  "OpenFace",
  "DeepFace",
  "DeepID",
  "ArcFace",
  "Dlib",
  "SFace",
  "GhostFaceNet",
]

backends = [
  'opencv',
  'ssd',
  'dlib',
  'mtcnn',
  'fastmtcnn',
  'retinaface',
  'mediapipe',
  'yolov8',
  'yunet',
  'centerface',
]

def detect_emotion(img): 
        predictions = DeepFace.analyze(img, actions = ['emotion'], detector_backend=backends[1])
        emotion_prediction = predictions[0]["dominant_emotion"]
        print("Prediction: ", emotion_prediction)
        return emotion_prediction

if __name__ == "__main__":
    webcam_capture = cv.VideoCapture(0)
    while True:
        x, img = webcam_capture.read()
        emotion_prediction = detect_emotion(img, enforce_detecntion = False)

        cv.putText(img, emotion_prediction, (50,50), cv.FONT_HERSHEY_COMPLEX, 1, (255,255,255), 1, 2)
        cv.imshow("window", img)

        if emotion_prediction != None:
            print(emotion_prediction)

        key = cv.waitKey(20)
        if key == 27: # exit on ESC
            break



    cv.destroyWindow("window")
    webcam_capture.release()
