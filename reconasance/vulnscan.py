#!/usr/bin/env python3

import os, sys
import socket
from termcolor import colored

ip = input("Enter host to scan: ") or "172.16.122.131"
ports = [21,22,23,25,80,443,110]
default_timeout = 5

def get_banner(ip, port):
    try:
        socket.setdefaulttimeout(default_timeout)
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            result = s.connect_ex((ip, port))
            print(result)
            if result == 0:
                return s.recv(1024)
            else:
                print(colored("[-] IP %s/%d has no results" % (ip, port), "red"))

    except socket.timeout:
        print(colored("[-] TimeOut for %s/%d" % (ip, port), "red"))

    except ConnectionRefusedError:
        print("Connection was refused")
        pass
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
            exit(0)

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
