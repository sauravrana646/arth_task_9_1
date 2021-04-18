import speech_recognition as sr
import time


def takeCommand():

    r = sr.Recognizer()

    with sr.Microphone() as source:

        print("\nListening...")
        r.pause_threshold = 1
        audio = r.listen(source)
        print("OK...")

    try:
        print("Recognizing...")
        query = r.recognize_google(audio, language='en-in')
        print(f"User said: {query}\n")
        time.sleep(2)

    except Exception as e:
        print(e)
        print("Unable to Recognizing your voice.")
        return "None"

    return query
