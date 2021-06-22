import speech_recognition as sr
import pyaudio

r = sr.Recognizer()

keyWord = 'spot'

print(sr.Microphone.list_microphone_names())
with sr.Microphone(0) as source:
    print('Please start speaking..\n')
    while True: 
        audio = r.listen(source)
        try:
            print("Processing...")
            text = r.recognize_google(audio)
            print("...Finished")
            if keyWord.lower() in text.lower():
                print('Keyword detected in the speech.')
                print(text)
            else:
                print("fail {0}", text)
        except Exception as e:
            print('Please speak again.')