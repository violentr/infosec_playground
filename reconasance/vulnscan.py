#!/usr/bin/env python3

import os, sys
import socket
from termcolor import colored

ip = "172.16.122.131"
ports = [21,22,23,25,80,443,110]

def get_banner(ip, port):
    try:
        socket.setdefaulttimeout(2)
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.connect((ip, port))
        return sock.recv(1024)

    except socket.timeout:
        print(colored("Time is up", "red"))
    except ConnectionRefusedError:
        pass
        #print("Connection was refused")
    except KeyboardInterrupt:
        print(colored("Crl + C was pressed", 'red'))
        exit(0)

def checkVuln(banner, filename):
    try:
        banner = banner.decode('UTF-8')
        with open(filename) as f:
            for line in f.readlines():
                if line.strip("\n") in banner:
                    print("Server is vulnerable to: %s" % banner)
    except UnicodeDecodeError:
        print(colored("can't decode using UTF-8", 'red'))

def main():
    global ip, ports

    if len(sys.argv) == 2:
        filename = sys.argv[1]
        if not os.path.isfile(filename):
            print(colored("[-] File %s does not exist" % filename, 'red'))
        if not os.access(filename, os.R_OK):
            print(colored("[-] Access is denied!", 'red'))
            exit(0)
    else:
        print("Usage: %s <vulns filename>" % sys.argv[0])
        exit(0)
    for port in ports:
        banner = get_banner(ip, port)
        if banner:
            print("[+] %s/%d" %(ip,port))
            checkVuln(banner, filename)

if __name__ == '__main__':
    main()
