import os
from chk_run import check
from AWS.ec2 import ec2
from AWS.s3 import s3
from AWS.cloudfront import cloudfront
from welcome import welcome
from colorama import Fore, Back, Style
from tts import speak
from subprocess import run, PIPE
from takecmd import takeCommand


def aws():
    os.system("clear")
    print(welcome("AWS"))
    aws_out = run(f"aws help", shell=True, capture_output=True)
    if aws_out.returncode != 0:
        speak("AWS CLI is not installed on the machine")
        print(Fore.RED + f"AWS CLI is not installed on the machine\nError : \n{aws_out.stderr.decode()}")
        print(Style.RESET_ALL)
        speak("Exiting...\n\nPress ENTER to continue...")
        print("Exiting...\n\nPress ENTER to continue...")
        input()
        return
    else:
        pass
    speak("Checking User Authetication....Please Wait")
    print("\nChecking User Authentication\n")
    authcheck = run("aws sts get-caller-identity",shell=True, capture_output=True)
    if authcheck.returncode == 0:
        print(Fore.GREEN + f"\nAlready Authenticated\n\n{authcheck.stdout.decode()}")
        speak("Already Autheticated...")
        print(Style.RESET_ALL)
    else:
        speak("No Login Found... First you will need to login...")
        print("No Login Found\nFirst you need to login to aws\n")
        auth = run("aws configure", shell=True, stderr=PIPE)
        authout = run("aws sts get-caller-identity",shell=True, capture_output=True)
        if auth.returncode == 0 and authout.stdout.decode() not in [" ", ' ', '', ""]:
            speak("Authentication Successfull")
            print(Fore.GREEN + f"\nAuthentication succcess\n\n{authout.stdout.decode()}")
            print(Style.RESET_ALL)
        else:
            speak("Couldn't Authenticate...")
            print(Fore.RED + f"\nCouldn't authenticate\n\nError : \n{authout.stderr.decode()}")
            print(Style.RESET_ALL)
    speak("Press ENTER to continue...")
    input("Press ENTER to continue....")

    while True:
        os.system("clear")
        print(welcome("AWS"))
        speak("Welcome to AWS...")
        speak("Select from Below")
        print("""Select from below : 
        COMPUTE (EC2)
        STORAGE (S3)
        Cloundfront
        Go back""")
        cmd_text = takeCommand()
        cmd_list = cmd_text.lower().split()
        if check(cmd_list) and 'compute' in cmd_list:
            ec2()
        if check(cmd_list) and 'storage' in cmd_list:
            s3()
        if check(cmd_list) and 'cloudfront' in cmd_list:
            cloudfront()
        elif any(item in ["back" , "go back" ] for item in in cmd_list):
            return
        os.system("clear")
