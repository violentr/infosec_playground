#!/bin/bash

network=network.txt
hosts=live_hosts.txt
green='\033[0;32m'
esc='\033[0m'

printf "Scanning network $1 please standy\n"
nmap $1 -n -vvv -sn | grep report | awk '{print $5}' > $network

printf "${green}[+] Network scan completed - [ $network ] created ${esc}\n"

printf "${green}[+] File created - [ $hosts ]  created ${esc}\n"
printf "Found live hosts:\n\n"

arp -an | sed '/\(incomplete\)/d' | tee $hosts
#arp -a -n | awk '{print $2 $4}' | sed '/\(incomplete\)/d'
