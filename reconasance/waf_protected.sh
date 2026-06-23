#!/usr/bin/env bash
#
# Coded by violentR
# Check if IP is protected with CF / AKAMAI etc
# Install:  httpx is https://github.com/projectdiscovery/httpx

if [[ $# -eq 0 ]]; then
    echo "No File was provided."
    echo "Usage: ./waf_protected file_with_hostnames"
    exit 1
fi
echo -e "Cleaning up .. "

prefix="WAF"
outputFile="$prefix-output_ips.txt"
file=$1

rm $outputFile 2>/dev/null
rm $prefix-output.txt 2>/dev/null
rm $prefix-real_ips.txt 2>/dev/null
rm $prefix-raw_report.txt 2>/dev/null
rm $prefix-report.txt 2>/dev/null

echo -e "\nSTAGE 1: Checking for public domains"

cat $file | httpx -probe | tee -a $prefix-output.txt

echo -e "\nSTAGE 2: Saving data to $outputFile"
cat output.txt | grep SUCCESS | cut -d " " -f1 | httpx -ip | tee -a $prefix-raw_report.txt
cat raw_report.txt | cut -d "[" -f1 | cut -d "/" -f3 | httpx -ip > $outputFile

cat $outputFile | cut -d "[" -f2 |tr "]" " " | sort -u > $prefix-real_ips.txt

echo -e "\nSTAGE 3: Checking if ip sits behind WAF"
while read -r ip;do orgName=$(curl -ks https://ipinfo.io/$ip | jq '.org'); echo "$line - $orgName" | tee -a $prefix-report.txt;done<$prefix-real_ips.txt
