import speech_recognition as sr

r = sr.Recognizer() 

def detect_wav(wav_file):    
        with sr.AudioFile(wav_file) as source2:
            print("Listening")
            audio2 = r.listen(source2)
            MyText = r.recognize_google(audio2)
            MyText = MyText.lower()

            return MyText
        

if __name__ == "__main__":
    print(detect_wav("/Users/rohitchavali/Desktop/Verbalflow/recordedFiles/audio.wav"))