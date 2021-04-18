from subprocess import Popen,PIPE,run
from welcome import welcome
import sys
from os import system
from tts import speak
from takecmd import takeCommand
from colorama import Fore, Back, Style

def create_partition(device,part_type="",part_number="",start="",end="") :
    part_out = run(f"fdisk {device}",capture_output=True,shell=True,input=f"n\n{part_type}\n{part_number}\n{start}\n{end}\ny\nw\n",text=True,encoding='ascii')
    if part_out.returncode == 0:
        for line in part_out.stdout.split("\n"):
            if line.startswith("Created") : 
                    print()
                    print(Fore.GREEN + line)
                    print(Style.RESET_ALL)
        speak("Succcessfully Created the partition")
        print(Fore.GREEN + f"Succcessfully Created the partition\n")
        print(Style.RESET_ALL)
    else :
        print(Fore.RED + f"\nCouldn't create partition\n\nError : \n{part_out.stderr}")
        speak("couldn't create partition")
        print(Style.RESET_ALL)

    input("\nPress ENTER to continue...")

def delete_partition(device,part_number):
    delpart_out = run(f"fdisk {device}",capture_output=True,shell=True,input=f"d\n{part_number}\nw",text=True,encoding='ascii')
    if delpart_out.returncode == 0:
        for line in delpart_out.stdout.split("\n"):
            if line.startswith("Partition") : 
                    print()
                    print(Fore.GREEN + line)
                    print(Style.RESET_ALL)
        print(Fore.GREEN + f"Succcessfully deleted the partition\n")
        speak("Successfully deleted partiton...")
        print(Style.RESET_ALL)
    else :
        print(Fore.RED + f"\nCouldn't delete partition\n\nError : \n{delpart_out.stderr.decode()}")
        speak("Couldn't delete partition...")
        print(Style.RESET_ALL)
    input("\nPress ENTER to continue...")
def partition():    
    while True:
        system("clear")
        print(welcome("LINUX PARTITIONS"))
        speak("Welcome to partitions...")
        speak("select from below...")
        print("""Select from below : 
        1. Create new partition
        2. Delete partition
        3. List partitions
        9. Go back""")

        cmd_text = takeCommand()
        cmd_list = cmd_text.lower().split()

        if "create partition" in cmd_list :
            print("\nListing all Devices : \n")
            speak("Listing all Devices")
            print_out = run(f"fdisk -l",capture_output=True,shell=True)
            print_out = print_out.stdout.decode(sys.stdout.encoding)
            for line in print_out.split("\n"):
                if line.startswith("Disk /dev/s") : 
                    print(f"\n{line}")
            speak("Choose a disk...")
            device = input("\n\nEnter Disk Name [ex : /dev/sda]: ")
            print(f"\n\nPrinting Already Created Partitions in {device}\n")
            speak(f"Printing partitions in {device}")
            print_out = run(f"fdisk {device}",capture_output=True,shell=True,input=b'p\nq\n')
            print_out = print_out.stdout.decode(sys.stdout.encoding)
            for line in print_out.split("\n"):
                if line == "Device does not contain a recognized partition table.":
                    print(Fore.RED + "No partitions Found")
                    speak("No Partitions found...")
                    print(Style.RESET_ALL)
                    break
                if line.startswith("/") or line.startswith("Device"): 
                    print(line)
                else : 
                    continue
            part_type = input("\n\nEnter partition type [primary p \ extended e] : ")
            part_number = input("Enter partition number (leave empty for default): ")
            start = input("Enter start sector (leave empty for default) : ")
            end = input("Enter last sector (leave empty for default or can give size as +5G) : ")
            create_partition(device,part_type,part_number,start,end)
        if "delete partition" in cmd_list :
            print("\nListing all Devices : \n")
            speak("Listing all Devices")
            print_out = run(f"fdisk -l",capture_output=True,shell=True)
            print_out = print_out.stdout.decode(sys.stdout.encoding)
            for line in print_out.split("\n"):
                if line.startswith("Disk /dev/s") : 
                    print(f"\n{line}")
            speak("Choose a Disk")
            device = input("\n\nEnter Disk Name [ex : /dev/sda]: ")
            print(f"\n\nPrinting Partitions in {device}\n")
            speak(f"Printing Partitions in {device}")
            print_out = run(f"fdisk {device}",capture_output=True,shell=True,input=b'p\nq\n')
            print_out = print_out.stdout.decode(sys.stdout.encoding)

            for line in print_out.split("\n"):
                if line == "Device does not contain a recognized partition table.":
                    print(Fore.RED + "No partitions Found")
                    speak("No partitions Found")
                    print(Style.RESET_ALL)
                    input("\nPress ENTER to continue..")
                    partition()
                if line.startswith("/") or line.startswith("Device"): 
                    print(line)
                else : 
                    continue
            
            part_number = input("\nEnter partition number to delete (leave empty for default): ")
            speak("Enter partition Number to delete") 
            delete_partition(device,part_number)
            
        if all(item in ['list','partitions'] for item in cmd_list) or all(item in ['list','partition'] for item in cmd_list) :
            print(Fore.GREEN + "\n\nPrinting Partitions")
            speak("Printing Partitions...")
            print(Style.RESET_ALL)
            print_out = run(f"fdisk -l",capture_output=True,shell=True)
            print_out = print_out.stdout.decode(sys.stdout.encoding)
            for line in print_out.split("\n"):
                if line.startswith("Disk /dev/s") : 
                    print(f"\n{line}")
                if line.startswith("Device") : 
                    print(f"\n{line}")
                elif line.startswith("/") : 
                    print(line)       
            input("\nPress Enter to continue...")

        elif any(item in ["back" , "go back" ] for item in in cmd_list):
            return

        system("clear")

