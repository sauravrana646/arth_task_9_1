import pyttsx3


engine = pyttsx3.init('sapi5')
voices = engine.getProperty('voices')
engine.setProperty('voice', 'voices[0].id')
engine.setProperty('rate', 145)
engine.setProperty('volume', 0.8)


def speak(text):
    engine.say(text)
    engine.runAndWait()
