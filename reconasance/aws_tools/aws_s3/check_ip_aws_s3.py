#!/usr/bin/env python3
import sys
import ipaddress

def is_ip_in_range(ip, cidr):
    network = ipaddress.ip_network(cidr)
    ip_address = ipaddress.ip_address(ip)
    return ip_address in network

def main():
    ip_to_check = sys.argv[1]
    cidr_range = sys.argv[2]

    if is_ip_in_range(ip_to_check, cidr_range):
        print(f"The IP address {ip_to_check} is in the range {cidr_range}.")
        return 0
    #else:
    #    print(f"The IP address {ip_to_check} is NOT in the range {cidr_range}.")

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python script.py <IP_ADDRESS> <CIDR_RANGE>")
        sys.exit(1)
    else:
        main()

