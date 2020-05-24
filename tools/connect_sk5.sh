#!/usr/bin/env bash
proxyPort=
remoteHost=
sshKey=

function doCheck(){
  [ -z $proxyPort ] && echo -e "[-] No socks5 port defined" && exit 1
  [ -z $remoteHost ] && echo -e "[-] No remote host defined" && exit 1
  [ -z $sshKey ] && echo -e "[-] No SSH key defined" && exit 1
}

doCheck
curPid=$(lsof -i TCP:$proxyPort | awk '/LISTEN/ {print $2}')

if [ ! -z "$curPid" ];then
  echo -e "[+] Closing previously opened proxy port: $proxyPort"
  kill -9 $curPid
fi

echo -e "Connecting to remote host: $remoteHost"
ssh -D $proxyPort -i $sshKey -N -f ubuntu@$remoteHost

echo -e "[+] Proxing local traffic through socks5, port: $proxyPort\n"

netstat -ant |grep LISTEN |grep $proxyPort
echo -e "\n[+] Run this command now: export http_proxy=socks5://127.0.0.1:$proxyPort"
