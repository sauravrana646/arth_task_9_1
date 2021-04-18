from wishme import wishMe
from takecmd import takeCommand
from tts import speak
from chk_run import run_command,check
import speech_recognition as sr
from welcome import welcome
from AWS.aws import aws
from Partitions.partiton import partition
import os


def main():
    while True:
        os.system("clear")
        print(welcome("ARTH TASK"))
        speak("Choose a service")
        print("\nChoose service you want to use : ")
        print("""
        CLOUD (AWS)
        PARTITION
        LVM
        DOCKER
        MACHINE LEARNING
        YUM (Recommended first if not configured)
        HADOOP
        BROWSER
        EXIT/LEAVE
        """
              )
        cmd_text = takeCommand()
        cmd_list = cmd_text.lower().split()
        if (check(cmd_list) and "cloud" in cmd_list) or "cloud" in cmd_list :
            aws()
        elif (check(cmd_list) and "partition" in cmd_list) or "partition" in cmd_list :
            print("Ok partitions")
            partition()
        elif any(item in cmd_list for item in ["leave", "exit", "goodbye"]):
            return 0


def wakeCommand():
    while True:
        query = ""
        wake_text = "wake up"
        r = sr.Recognizer()
        retcode = None
        with sr.Microphone() as source:
            r.pause_threshold = 1
            audio = r.listen(source)
        try:
            query = r.recognize_google(audio, language='en-in')
        except:
            pass

        if query == wake_text:
            wishMe()
            retcode = main()
        if retcode == 0:
            speak("Exiting...Wake me up if you need me")
            wakeCommand()


if __name__ == "__main__":
    wakeCommand()
