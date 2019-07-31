#!/usr/bin/env python3
#usage  ./scanner.py -H 172.16.122.131 -p 22,80,135
import socket
from socket import gethostbyname, gethostbyaddr, setdefaulttimeout
import sys
import optparse
from termcolor import colored
from threading import Thread

threads = []
# tcp - socket.SOCK_STREAM
# udp - socket.SOCK_DGRAM

def conn_scan(ip, port):
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.connect((ip, port))
        msg = "tcp/%d open" % port
        print(colored(msg, "green"))

    except socket.error:
        msg = "tcp/%d closed" % port
        print(colored(msg, "red"))
        sys.exit()
    except socket.gaierror:
        print('Hostname could not be resolved. Exiting')
        sys.exit()
    except KeyboardInterrupt:
        print("You pressed Ctrl+C")
        sys.exit()

def port_scan(host, ports):
    setdefaulttimeout(1)
    try:
        ip = gethostbyname(host)
        print('[+] results for ip %s' % ip)
    except:
        print('[+] unable to resolve ip %s' % ip)

    for port in ports:
        t = Thread(target=conn_scan, args=(ip, int(port)))
        threads.append(t)
        t.start()

def program_options():
    parser = optparse.OptionParser('Usage : -H <target host> -p <target port>')
    parser.add_option('-H', dest='target_host', type='string', help='define host to scan')
    parser.add_option('-p', dest='target_port', type='string', help='define port separated by coma')
    return parser

def cleanup():
    global threads
    return [thread.join() for thread in threads]

def main():
    parser = program_options()
    (options, args) = parser.parse_args()
    target_host = options.target_host
    target_ports = str(options.target_port).split(',')
    if (target_host == None) | (target_ports[0] == None):
        print(parser.usage)
        exit(0)

    port_scan(target_host, target_ports)

if __name__ == '__main__':
    main()
    cleanup()
