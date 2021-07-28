import speech_recognition as sr

def main():
    recognizer = sr.Recognizer()
    mic = sr.Microphone(device_index=0)
    while True:
        response = recognize_speech_from_mic(recognizer, mic)
        print('\nSuccess : {}\nError   : {}\n\nText from Speech\n{}\n\n{}' \
            .format(response['success'],
                response['error'],
                '-'*17,
                response['transcription']))

def recognize_speech_from_mic(recognizer, microphone):
    if not isinstance(recognizer, sr.Recognizer):
        raise TypeError("`recognizer` must be `Recognizer` instance")

    if not isinstance(microphone, sr.Microphone):
        raise TypeError("`microphone` must be `Microphone` instance")

    with microphone as source:
        recognizer.adjust_for_ambient_noise(source)
        audio = recognizer.listen(source)

    response = {
        "success": True,
        "error": None,
        "transcription": None
    }

    try:
        response["transcription"] = recognizer.recognize_google(audio)
    except sr.RequestError:
        response["success"] = False
        response["error"] = "API unavailable/unresponsive"
    except sr.UnknownValueError:
        response["error"] = "Unable to recognize speech"

    return response

main()