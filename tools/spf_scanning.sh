#!/usr/bin/env bash

#Scanning ports with hping3
#Spoof your ip and scan of your target
#Make bigger delay to be more stealthier

output_file="results.txt"

tool="$(hping3 -h 2>/dev/null)"
[[ -z "$tool" ]] && echo -e "[-] hping3 should be installed" && exit 1

[[ -f $output_file ]] && (rm $output_file && echo "[+] Deleted ./$output_file")

ports="80 900 8008 8443"
spoofed_ip="192.168.1.201"
target_ip="192.168.1.100"

for port  in $ports
do
  echo -e "\n[+] Scanning Port: $port"
  output="$(hping3 -S -p $port -a $spoofed_ip $target_ip -c 1)"
  result="$(echo $output | grep -o "flags=SA")"
  [[ ! -z "$result" ]] && (echo "Port $port is open" >> $output_file)
  sleep 5
done

echo -e "\nScan is completed:"
echo -e "[+] Output was saved to ./$output_file\n"
cat $output_file
