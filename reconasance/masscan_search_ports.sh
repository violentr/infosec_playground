#!/bin/bash
# Copyright by Deniss 
# Search for tcp ports from masscan output_4_* files
# Navigate to the folder where files output_4_* were saved
# Run ./masscan_search_ports.sh | sort -u

ports=("22" "80" "443" "3306")

for file in $(ls | grep "output_4_")
  do
  for port in "${ports[@]}";
    do
    cat $file | grep -Eo "$port/tcp on [0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}"
    done
done
