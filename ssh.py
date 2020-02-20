import os
import ctypes
import json
import time
import sys
from paramiko import SSHClient, AutoAddPolicy
from colorama import Fore, Back, Style
from tabulate import tabulate
from tkinter import Tk, filedialog

class SSH_Server(object):
    def __init__(self, ssh_credentials: list):
        self.ssh_credentials = ssh_credentials
        self.SSH = SSHClient()
    
    def connect_to_ssh_server(self, ssh_policy=AutoAddPolicy) -> bool:
        self.SSH.set_missing_host_key_policy(ssh_policy)
        self.SSH.load_system_host_keys()        
        try:
            self.SSH.connect(username=self.ssh_credentials[1],
                        password=self.ssh_credentials[2], 
                        hostname=self.ssh_credentials[0])
            if self.SSH:                
                return True
        except Exception as SSH_Error:
            print(Fore.RED + "%s%s%s" % (chr(32)*4, SSH_Error, chr(32)*10))
            return False
    
    def ssh_exec_command(self, unix_command: str) -> tuple:
        if unix_command != "" or unix_command != None:
            return self.SSH.exec_command(unix_command, get_pty=True)
        return ('','','')

    def download_local_remote_file(self, remote_file_path: list, local_file_path: list, option: str) -> bool:
        sftp = self.SSH.open_sftp()
        try:
            for i in range(len(local_file_path)):
                if option == "--upload-local-file":
                    sftp.put(local_file_path[i], remote_file_path[i])
                    print(Fore.LIGHTWHITE_EX + "%s%s" % (chr(32)*5, "Uploading '%s'" % local_file_path[i]))
                elif option == "--download-remote-file":
                    sftp.get(remote_file_path[i], local_file_path[i])
                    print(Fore.LIGHTWHITE_EX + "%s%s" % (chr(32)*5, "Downloading '%s'" % remote_file_path[i]))
            sftp.close()
            return True
        except Exception as sftp_error:
            print(Fore.RED + "%s%s%s" % (chr(32)*5, sftp_error, chr(32)*10))
            return False
    
    def close_ssh(self, option: bool) -> bool:
        self.SSH.close()
        return True
        
def micro_stamp(text: str) -> str:
    print("%s" % "\n")
    for each_char in text:
        sys.stdout.write(each_char)
        sys.stdout.flush()
        time.sleep(0.015)

def get_ssh_credentials(config_file: dict) -> list:
    ssh_credentials = []
    ssh_cred_headers = []
    for each_credentials in config_file["SSH"]["Default"]:
        ssh_cred_headers.append(each_credentials)
        ssh_credentials.append(config_file["SSH"]["Default"][each_credentials])
    return (ssh_credentials, ssh_cred_headers)

def get_file_paths(option: str) -> list:
    if option == "--upload-local-file":
        remote_file_paths_list = []
        local_file_paths_list = []
        remote_path = input(Fore.GREEN + "%s~ %s: " % (chr(32)*5, "Specify Remote Path"))
        root = Tk()
        root.withdraw()
        root.fileName = filedialog.askopenfilenames(filetype = (("Text Files","*.txt"),("All Files","*.*")))
        try:
            if root.fileName != "":
                print(Fore.LIGHTYELLOW_EX + "%s%s: " % (chr(32)*5, "Local Files"))
                for each_local_files in root.fileName:
                    print(Fore.YELLOW + "%s%s" % (chr(32)*5, each_local_files))
                    local_file_paths_list.append(each_local_files)
                    remote_file_paths_list.append(r"%s/%s" % (remote_path, os.path.basename(each_local_files)))
                cont = input(Fore.LIGHTBLUE_EX + "%s%s: " % (chr(32)*5, "Continue Uploading? (Y/N)"))
                if cont == "Y" or cont == "y":
                    return [remote_file_paths_list, local_file_paths_list]
                else:
                    print(Fore.RED + "%s%s" % (chr(32)*5, "File uploads terminated ..."))
                    return False
            else:
                print(Fore.RED + "%s%s" % (chr(32)*5, "Please specify file to upload ..."))
                return False
        except Exception:
            pass
    elif option == "--download-remote-file":
        remote_file_path = input(Fore.GREEN + "%s~ %s: " % (chr(32)*5, "Remote File Path"))
        local_path = input(Fore.GREEN + "%s~ %s: " % (chr(32)*5, "Specify Local Path"))
        remote_file_name = os.path.basename(remote_file_path)
        if remote_file_path != "" and local_path != "":
            cont = input(Fore.LIGHTBLUE_EX + "%s%s: " % (chr(32)*5, "Continue Downloading? (Y/N)"))
            if cont == "Y" or cont == "y":
                return [[remote_file_path], [r"%s\%s" % (local_path, remote_file_name)]]
            else:
                print(Fore.RED + "%s%s" % (chr(32)*5, "File uploads terminated ..."))
                return False
        else:
            print(Fore.RED + "%s%s" % (chr(32)*5, "Please specify file to download ..."))

# customize terminal window, set title and adjust terminal width and height
os.system("mode con cols=80 lines=40")
ctypes.windll.kernel32.SetConsoleTitleW("FrontLine ~ SSH Server")

# load __ssh_config__.json and banner file
with open(file=r"__ssh_config__.json", mode="r", encoding="utf-8") as ssh_config:
    config_file = json.loads(ssh_config.read())
    ssh_config.close()

# load banner file from configurations and message
print(Fore.LIGHTGREEN_EX + open(file=r"%s" % config_file["SSH"]["Banner"], mode="r", encoding="utf-8").read())
time.sleep(1.5)
micro_stamp(Fore.YELLOW + "%s%s" % (chr(32)*4, config_file["SSH"]["Message"]))
time.sleep(0.05)

# start of the actual program
# =================================
# https://github.com/IAmArien
# =================================

if __name__ == "__main__":
    print(Fore.MAGENTA + "\n\n%s%s" % (chr(32)*4, "Connecting to SSH Server, Please wait ..."), end="\r", flush=True)
    time.sleep(0.05)
    ssh_credentials = get_ssh_credentials(config_file)[0]
    ssh_cred_headers = get_ssh_credentials(config_file)[1]
    ssh_connection = SSH_Server(ssh_credentials)
    if ssh_connection.connect_to_ssh_server():
        print(Fore.LIGHTBLUE_EX + "%s%s" % (chr(32)*4, "Connected Successfully to SSH Server: %s@%s:%s" % (ssh_credentials[1], ssh_credentials[2], ssh_credentials[0])))
        time.sleep(1)
        ssh_credentials.append(22)
        ssh_cred_headers.append("SSH Port")
        for each_tab_data in str(tabulate(tabular_data=[ssh_credentials], headers=ssh_cred_headers, tablefmt="fancy_grid")).split("\n"):
            print("%s%s" % (chr(32)*4, each_tab_data))
        time.sleep(0.5)
        print("\n")
        while True:
            try:
                unix_command = input(Fore.GREEN + "%s%s@%s:~> " % (chr(32)*4, ssh_credentials[1], ssh_credentials[0]) + Fore.LIGHTYELLOW_EX)
                if unix_command == "--upload-local-file" or unix_command == "--download-remote-file":
                    file_paths = get_file_paths(option=unix_command)
                    if file_paths is not False:
                        ssh_connection.download_local_remote_file(remote_file_path=file_paths[0], local_file_path=file_paths[1], option=unix_command)
                    continue
                elif unix_command.lower() == "exit":
                    if ssh_connection.close_ssh(True):
                        print(Fore.RED + "%s%s" % (chr(32)*4, "Terminating Script ..."))
                        time.sleep(3)
                        print(Style.RESET_ALL)
                        sys.exit(0)
                elif unix_command.lower() == "clear":
                    os.system("cls")
                    continue
                stdin, stdout, stderr = ssh_connection.ssh_exec_command(unix_command=unix_command)                
                for line in iter(stdout.readline, ""):
                    print("%s%s" % (chr(32)*4, line), end="")
            except Exception as exc:
                print(Fore.RED + "%s%s" % (chr(32)*4, exc))
    else:
        time.sleep(3)
        sys.exit(0)    
