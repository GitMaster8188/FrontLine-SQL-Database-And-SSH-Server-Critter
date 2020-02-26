import json as json
import time as time
import os as os
import ctypes as ctypes
import cx_Oracle as oracle_db
import sys as sys
from colorama import Fore, Back, Style
from tabulate import tabulate

class Oracle_DB(object):
    def __init__(self, oracle_credentials: dict):
        super().__init__()
        self.oracle_credentials = oracle_credentials
        self.oracle_connection = None
    
    def connect_to_oracle_db(self, passphrases: list) -> oracle_db.Cursor:
        for i in range(len(self.oracle_credentials)):
            temp_cred_keys = []
            for each_keys in self.oracle_credentials.keys():
                temp_cred_keys.append(each_keys)
            self.oracle_credentials[temp_cred_keys[i]] = passphrases[i]        
        try:
            self.oracle_connection = oracle_db.connect("%s/%s@%s:%s/%s" % (self.oracle_credentials["username"],
                                                self.oracle_credentials["password"], self.oracle_credentials["hostname"],
                                                self.oracle_credentials["port"], self.oracle_credentials["database"]))
            if self.oracle_connection:
                return self.oracle_connection.cursor()
            else:
                return False
        except oracle_db.DatabaseError as oracle_conn_err:
            print(oracle_conn_err)
            return False
    
    def close_oracle_connection(self, option: bool) -> bool:
        self.oracle_connection.close()
        return True

# customize terminal window, set title and adjust terminal width and height
os.system("mode con cols=80 lines=40")
ctypes.windll.kernel32.SetConsoleTitleW("FrontLine ~ Oracle SQL Database Server")

# load __oracle_config__.json and banner file
with open(file=r"__oracle_config__.json", mode="r", encoding="utf-8") as oracle_config:
    config_file = json.loads(oracle_config.read())
    oracle_config.close()

# load banner file from configurations and message
print(Fore.CYAN + open(file=r"%s" % config_file["Oracle"]["Banner"], mode="r", encoding="utf-8").read())
time.sleep(0.05)
print(Fore.LIGHTYELLOW_EX + "\t\t\t     SQL Database Server")
time.sleep(0.05)
print(Fore.LIGHTRED_EX + "\t╬╬╬ Let's dig into database structures and millions of data ╬╬╬")
time.sleep(0.05)
print(Fore.LIGHTGREEN_EX + "\t\t\t\tIAmArien8188")
time.sleep(1.5)

# passphrases
oracle_passphrases = {
    "hostname": "",
    "username": "",
    "password": "",
    "port": 0,
    "database": ""
}

# assign credentials from config file
temp_oracle_credentials = []
for each_cred in config_file["Oracle"]["Default"]:
    temp_oracle_credentials.append(config_file["Oracle"]["Default"][each_cred])

# start of the actual program
# =================================
# https://github.com/IAmArien
# =================================

if __name__ == "__main__":
    oracle = Oracle_DB(oracle_credentials=oracle_passphrases)
    print(Fore.LIGHTMAGENTA_EX + "\n%s%s" % (chr(32)*5, "Connecting to Oracle SQL Database, Please wait ..."), end="\r", flush=True)
    cursor = oracle.connect_to_oracle_db(temp_oracle_credentials)
    if cursor:
        print(Fore.YELLOW + "%s%s" % (chr(32)*5, "Successfully Connected to " + Fore.LIGHTYELLOW_EX + "(%s/%s@%s:%s/%s)" % (oracle_passphrases["username"],
                                                oracle_passphrases["password"], oracle_passphrases["hostname"],
                                                oracle_passphrases["port"], oracle_passphrases["database"])))
        time.sleep(0.5)
        for each_tab_data in str(tabulate(tabular_data=[temp_oracle_credentials], headers=["Hostname", "Username", "Password", "Port", "Service Name"], tablefmt="fancy_grid")).split("\n"):
            print(Fore.LIGHTGREEN_EX + "%s%s" % (chr(32)*5, each_tab_data))
        time.sleep(1)
        print("\n")
        while True:
            try:
                oracle_sql = input(Fore.LIGHTCYAN_EX + "%s(Oracle) %s@%s:~> " % (chr(32)*5, temp_oracle_credentials[1], temp_oracle_credentials[4]) + Fore.LIGHTYELLOW_EX)
                if oracle_sql.lower() == "exit":
                    if oracle.close_oracle_connection(option=True):
                        print(Fore.RED + "%s%s" % (chr(32)*5, "Terminating Script ..."))
                        time.sleep(3)
                        print(Style.RESET_ALL)
                        sys.exit(0)
                elif oracle_sql.lower() == "clear":
                    os.system("cls")
                    continue
                command = cursor.execute(oracle_sql)
                col_names = [row[0] for row in cursor.description]
                data_array = []
                for each_data in command.fetchall():
                    data_array.append(each_data)
                for each_tab_data in str(tabulate(data_array, headers=col_names, tablefmt="psql")).split("\n"):
                    print(Fore.LIGHTYELLOW_EX + "%s%s" % (chr(32)*5, each_tab_data))
            except Exception as sql_error:
                print(Fore.RED + "%s%s" % (chr(32)*5, sql_error))

time.sleep(5)

