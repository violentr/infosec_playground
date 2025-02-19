#!/usr/bin/env bash
# Masscan for all TCP ports

input_file=$1
output_file="output_4_"

while read -r ip
do
echo "Scanning: $ip"
    sudo masscan -p0-65535 $ip --rate=10000 | tee -a "$output_file"_$ip.txt
done<$input_file
