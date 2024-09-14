import speech_recognition as sr


r = sr.Recognizer() 



def detect_wav(wav_file):    
    try:
        with sr.AudioFile(wav_file) as source2:
            print("Listening")
            audio2 = r.listen(source2)
            MyText = r.recognize_google(audio2)
            MyText = MyText.lower()

            print(MyText)
            
    except sr.RequestError as e:
        print("Unable to recognize audio. ")
        
    except sr.UnknownValueError:
        print("Unknown file value. File not found/File Corrupted. ")
