#!/usr/bin/env bash

# Check port <address> <port>
port_info(){
  echo "Port is open" || echo "Port is closed" || echo "Connection timeout"
}

check_port() {
  for app in nc curl telnet gtimeout timeout
  do
    if [ "$(which $app)" != "" ]; then
      tool=$app
      break
    else
      tool=devtcp
    fi
  done

  echo "Using '$tool' to test access to $1:$2"
  case $tool in
    nc) nc -v -G 5 -z -w2 $1 $2 ;;
    curl) curl -s --connect-timeout 10 http://$1:$2 ;;
    telnet) telnet $1 $2 ;;
    gtimeout)  gtimeout 1 bash -c "</dev/tcp/${1}/${2}" && port_info;;
    timeout)  timeout 1 bash -c "</dev/tcp/${1}/${2}" && port_info;;
    devtcp)  <"/dev/tcp/${1}/${2}" && port_info;;
    *) echo "no tools available to test $1 port $2";;
  esac
}
