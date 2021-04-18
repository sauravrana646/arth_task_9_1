import subprocess


go = ["open", "start", "run", "launch", "execute"]
nogo = ["donot", "do not", "don't", "not", "no", "dont"]


def check(cmd_list):
    if any(item in go for item in cmd_list) and not any(item in nogo for item in cmd_list):
        return True
    return False


def run_command(cmd_list, name, run_cmd):
    try:
        if check(cmd_list):
            print(f"{name}")
            subprocess.run(f"{run_cmd}", shell=True)
    except:
        print("Couldn't Run....Sorry")
