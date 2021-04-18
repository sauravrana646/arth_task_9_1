from subprocess import Popen,PIPE,run
from welcome import welcome
import sys
from tts import speak
from takecmd import takeCommand
from os import system
from colorama import Fore, Back, Style

def create_pv(devices):
    pvout = run(f"pvcreate {' '.join(devices)}",shell=True,input='y\n',encoding='ascii',stderr=PIPE)
    if pvout.returncode != 0 :
        print(Fore.RED + f"\n We encountered an error :\n{pvout.stderr.decode()}\n")
        speak("We encountered an error...")
        print(Style.RESET_ALL)
        print("Exiting...\n")
        speak("Exiting...")
        input("\nPress ENTER to continue ...")
        return
    print(Fore.GREEN + "\n\n Physical Volume Details :\n")
    speak("We encountered an error...")
    print(Style.RESET_ALL)
    run(f"pvdisplay {' '.join(devices)}",shell=True)    
    input("Press ENTER to continue ...")

def create_vg(vgname,pvname):
    vgout = run(f"vgcreate {vgname} {' '.join(pvname)}",input='y\n',encoding='ascii',shell=True,stderr=PIPE,text=True)

    if vgout.returncode != 0 :
        print(Fore.RED + f"\n We encountered an error :\n{vgout.stderr}\n")
        speak("We encountered an error...")
        print(Style.RESET_ALL)
        print("Exiting...\n")
        input("\nPress ENTER to continue ...")
        return
    print(Fore.GREEN + "\n\n Volume Group Details :\n")
    speak("Volume Group Details")
    print(Style.RESET_ALL)
    run(f"vgdisplay {vgname}",shell=True , stderr=PIPE)
    input("\nPress ENTER to continue ...")

def create_lv(lvname,lvsize,vgname):
    lvout = run(f"lvcreate --size {lvsize} -n {lvname} {vgname}",shell=True,capture_output=True)
    if lvout.returncode != 0 :
        print(Fore.RED + f"\n We encountered an error :\n{lvout.stderr.decode()}\n")
        speak("We encountered an error...")
        print(Style.RESET_ALL)
        print("Exiting...\n")
        input("\nPress ENTER to continue ...")
        return
    print(Fore.GREEN + "\n\n Logical Volume Details :\n")
    speak("Logical Volume Details")
    print(Style.RESET_ALL)
    run(f"lvdisplay /dev/{vgname}/{lvname}",shell=True , stderr=PIPE)
    input("\nPress ENTER to continue ...")

def extend_vg(vgname,pvname):
    vgex_out = run(f"vgextend {vgname} {' '.join(pvname)}",stderr=PIPE,shell=True)
    if vgex_out.returncode != 0 :
        print(Fore.RED + f"\n We encountered an error :\n{vgex_out.stderr}\n")
        speak("We encountered an error...")
        print(Style.RESET_ALL)
        print("Exiting...\n")
        input("\nPress ENTER to continue ...")
        return
    print(Fore.GREEN + "\n\n Volume Group Details :\n")
    speak("Volume Group Details")
    print(Style.RESET_ALL)
    run(f"vgdisplay {vgname}",shell=True , stderr=PIPE)
    input("\nPress ENTER to continue ...")

def extend_lv(lv_path,new_size):
    lvex_out = run(f"lvextend --size={new_size} {lv_path}",shell=True,stderr=PIPE)
    if lvex_out.returncode != 0 :
        print(Fore.RED + f"\n We encountered an error :\n{lvex_out.stderr}\n")
        speak("We encountered an error...")
        print(Style.RESET_ALL)
        print("Exiting...\n")
        input("\nPress ENTER to continue ...")
        return
    print(Fore.GREEN + "\n\nLogical Volume Details :\n")
    speak("Logical Volume Details")
    print(Style.RESET_ALL)
    run(f"lvdisplay {lv_path}",shell=True , stderr=PIPE)
    input("\nPress ENTER to continue ...")

def delete_lv(lv_path):
    del_out = run(f"lvremove {lv_path}",shell=True,stderr=PIPE,input='y\n',encoding='ascii')
    if del_out.returncode != 0 :
        print(Fore.RED + f"\n We encountered an error :\n{del_out.stderr}\n")
        speak("We encountered an error...")
        print(Style.RESET_ALL)
        print("Exiting...\n")
        input("\nPress ENTER to continue ...")
        return
    if del_out.returncode == 0:
        print(Fore.GREEN + "\nSuccessfully Deleted\n")
        speak("Successfully Deleted")
        print(Style.RESET_ALL)
        input("Press ENTER to continue...")

def del_vg(vgname):
    delvg_out = run(f"vgremove {vgname}",shell=True,stderr=PIPE,input='y\ny\n',encoding='ascii')
    if delvg_out.returncode != 0 :
        print(Fore.RED + f"\n We encountered an error :\n{delvg_out.stderr}\n")
        speak("We encountered an error...")
        print(Style.RESET_ALL)
        print("Exiting...\n")
        input("\nPress ENTER to continue ...")
        return
    if delvg_out.returncode == 0:
        print(Fore.GREEN + "\nSuccess\n")
        speak("success")
        print(Style.RESET_ALL)
        input("Press ENTER to continue...")

def del_pv(pvname):
    delpv_out = run(f"pvremove {' '.join(pvname)}",shell=True,stderr=PIPE)
    if delpv_out.returncode != 0 :
        print(Fore.RED + f"\n We encountered an error :\n{delpv_out.stderr}\n")
        speak("We encountered an error...")
        print(Style.RESET_ALL)
        print("Exiting...\n")
        input("\nPress ENTER to continue ...")
        return
    if delpv_out.returncode == 0:
        print(Fore.GREEN + "\nSuccess\n")
        speak("Success")
        print(Style.RESET_ALL)
        input("Press ENTER to continue...")


def lvm():    
    while True:
        system("clear")
        speak("Welcome To LVM")
        print(welcome("LVM PARTITION"))
        speak("Select from below")
        print("""Select from below :\n 
        Create Physical Volume
        Create Volume Group
        Create Logical Volume
        Extend Volume Group
        Extend Logical Volume
        Delete Logical Volume
        Delete Volume Group
        Delete Physical Volume
        Go back""")
        cmd_text = takeCommand()
        cmd_list = cmd_text.lower().split()

        if all(item in ["create","physical","volume"] for item in cmd_list) or "create physical volume" in cmd_text : 
            print(Fore.GREEN + "\n\nPrinting Available Device ")
            speak("Printing Available Devices")
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
            speak("Enter the device name")
            devices = input("\nEnter the name of device for PV (if multiple give space separated values) : ").split()
            print(f"\nTotal {len(devices)} entered : " , *devices)
            create_pv(devices)

        if  all(item in ["create","volume","group"] for item in cmd_list) or "create volume group" in cmd_text:
            speak("Enter Volume Group naem")
            vgname = input("Enter the name of VG to create : ")
            print(Fore.GREEN + "\nPrinting available PV ")
            print_pv = run(f"pvdisplay",capture_output=True,shell=True)
            print_pv = print_pv.stdout.decode().split("\n")
            for line in print_pv:
                if line.startswith("  PV Name") : 
                    print(line)
            print(Style.RESET_ALL)
            speak("Enter Physical Volume for VG")
            pvname = input("\nEnter Physical Volume (PV) device name to make VG : ").split()
            create_vg(vgname,pvname)

        if all(item in ["create","logical","volume"] for item in cmd_list) or "create logical volume" in cmd_text :
            speak("Enter Logical Volume Name")
            lvname = input("Enter the name of LV to create : ")
            speak("Enter the size")
            lvsize = input("Enter the size of LV (ex : 2G for 2GB size , 500M for 500 MB size ): ")
            print(Fore.GREEN + "\nPrinting available VG ")
            print_vg = run(f"pvdisplay",capture_output=True,shell=True)
            print_vg = print_vg.stdout.decode().split("\n")
            for line in print_vg:
                if line.startswith("  VG Name"):
                    print(line)
            print(Style.RESET_ALL)
            speak("Choose VG for LV")
            vgname = input("\nEnter the Volume Group (VG) name to make LV : ")
            create_lv(lvname,lvsize,vgname)

        if all(item in ["extend","volume","group"] for item in cmd_list) or "extend volume group" in cmd_text:
            ans = input(Fore.YELLOW + "\nCreating additional PV is recommended first\nDo you want to continue [y/n]: ")
            if ans.lower() != 'y' : 
                print(Style.RESET_ALL)
                return
            speak("Choose from available VG to extend")
            print(Fore.GREEN + "\nPrinting available VG ")
            print_vg = run(f"vgdisplay",capture_output=True,shell=True)
            print_vg = print_vg.stdout.decode().split("\n")
            for line in print_vg:
                if line.startswith("  VG Name"):
                    print(line)
            print(Style.RESET_ALL)
            vgname = input("\nEnter VG name to extend : ")
            print(Fore.GREEN + "\nPrinting available PV ")
            print_pv = run(f"pvdisplay",capture_output=True,shell=True)
            print_pv = print_pv.stdout.decode().split("\n")
            for line in print_pv:
                if line.startswith("  PV Name") : 
                    print(line)
            print(Style.RESET_ALL)
            speak("Choose Physical Volume to extend VG")
            pvname = input("\nEnter Physical Volume (PV) device name to extend VG : ").split()
            extend_vg(vgname,pvname)

        if all(item in ["extend","logical","volume"] for item in cmd_list) or "extned logical volume" in cmd_text:
            speak("Choose LV to extend")
            print(Fore.GREEN + "\nPrinting available LV ")
            print_lv = run(f"lvdisplay",capture_output=True,shell=True)
            print_lv = print_lv.stdout.decode().split("\n")
            # print(print_lv)
            for line in print_lv:
                if line.startswith("  LV Path"):
                    print(f"\n{line}")
                if line.startswith("  LV Name"):
                    print(line)
                if line.startswith("  LV Size"):
                        print(line)      
            print(Style.RESET_ALL)
            lv_path = input("Enter LV path which you want to extend : ")
            speak("Enter new size of LV")
            new_size = input("Enter new size of LV (8G for 8Gib): ")
            extend_lv(lv_path,new_size)
        
        if all(item in ["delete","logical","volume"] for item in cmd_list) or "delete logical volume" in cmd_text :
            print(Fore.GREEN + "\nPrinting available LV ")
            print_lv = run(f"lvdisplay",capture_output=True,shell=True)
            print_lv = print_lv.stdout.decode().split("\n")
            # print(print_lv)
            for line in print_lv:
                if line.startswith("  LV Path"):
                    print(f"\n{line}")
                if line.startswith("  LV Name"):
                    print(line)
                if line.startswith("  LV Size"):
                        print(line)      
            print(Style.RESET_ALL)
            speak("which LV you want to delete")
            lv_path = input("Enter LV path which you want to delete : ")
            delete_lv(lv_path)

        if all(item in ["delete","volume","group"] for item in cmd_list) or "delete volume group" in cmd_text:
            print(Fore.GREEN + "\nPrinting available VG ")
            print_vg = run(f"vgdisplay",capture_output=True,shell=True)
            print_vg = print_vg.stdout.decode().split("\n")
            for line in print_vg:
                if line.startswith("  VG Name"):
                    print(line)
            print(Style.RESET_ALL)
            speak("Which VG you want to delete")
            vgname = input("\nEnter VG name you want to delete : ")
            del_vg(vgname)
        if all(item in ["delete","physical","volume"] for item in cmd_list) or "delete physical volume" in cmd_text:
            print(Fore.GREEN + "\nPrinting available PV ")
            print_pv = run(f"pvdisplay",capture_output=True,shell=True)
            print_pv = print_pv.stdout.decode().split("\n")
            for line in print_pv:
                if line.startswith("  PV Name") : 
                    print(line)
            print(Style.RESET_ALL)
            speak("which PVs you want to delete")
            pvname = input("Enter PV name you want to delete (if multiple give space separated values) : ").split()
            del_pv(pvname)

        elif any(item in ["back" , "go back" ] for item in in cmd_list):
            return
        system("clear")

