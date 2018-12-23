#!/bin/bash

network=network.txt
hosts=live_hosts.txt
green='\033[0;32m'
red='\033[0;31m'
esc='\033[0m'
text='blank message'

greenMsg(){
  printf "${green} ${text} ${esc}\n"
}

redMsg(){
  printf "${red} ${text} ${esc}\n"
}


runCleanUp(){
  [[ -f $hosts ]] && echo "Running housekeeping.."
  if [ -f $hosts ]; then
    text="[-] Remove file $hosts $esc"
    redMsg
    rm $hosts
  fi
  if [ -f $network ]; then
    text="[-] Remove file $network $esc"
    redMsg
    rm $network
  fi
}

runCleanUp
printf "Scanning network $1 please standy\n"
nmap $1 -n -vvv -sn | grep report | awk '{print $5}' > $network

text="[+] Network scan completed - [ $network ] file created"
greenMsg
text="[+] Discovered live hosts - [ $hosts ] file created"
greenMsg
printf "Found live hosts:\n\n"

arp -an | sed '/\(incomplete\)/d' | tee $hosts
#arp -a -n | awk '{print $2 $4}' | sed '/\(incomplete\)/d'
