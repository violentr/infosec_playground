#!/usr/bin/env bash

proxyPort=8081
remoteHost=
sshKey=

echo -e "[+] Closing previously opened proxy port: $proxyPort"
lsof -i TCP:$proxyPort | awk '/LISTEN/ {print $2}' | xargs kill -9

echo -e "Connecting to remote host: $remoteHost"
ssh -D $proxyPort -i $sshKey -N -f ubuntu@$remoteHost

echo -e "[+] Proxing local traffic through socks5, port: $proxyPort\n"
export http_proxy=socks5://127.0.0.1:$proxyPort

netstat -antp |grep LISTEN |grep $proxyPort
