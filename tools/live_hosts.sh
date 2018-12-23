#!/bin/bash

outFile1=network.txt
outFile2=live_hosts.txt

printf "Scanning network $1 please standy\n"

nmap $1 -n -vvv -sn | grep report | awk '{print $5}' > $outFile1

printf "[+] Network scan completed - [ $outFile1 ] was created\n"

printf "Found live hosts:\n"

printf "[+] File - [ $outFile2 ]  was created\n"

arp -an | sed '/\(incomplete\)/d' | tee $outFile2
#arp -a -n | awk '{print $2 $4}' | sed '/\(incomplete\)/d'
