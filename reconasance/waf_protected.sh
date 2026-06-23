#!/usr/bin/env bash
#
# Coded by violentR
# Check if IP is protected with CF / AKAMAI
# Install:  httpx is https://github.com/projectdiscovery/httpx

if [[ $# -eq 0 ]]; then
    echo "No File was provided."
    echo "Usage: ./waf_protected file_with_hostnames"
    exit 1
fi

file=$1
prefix="WAF"
inputFile="$prefix-input.txt"
outputFile="$prefix-output.txt"

echo -e "\n Cleanning up previous files .."
rm $outputFile 2>/dev/null
rm $inputFile 2>/dev/null

echo -e "\n Preparing data for the look up .."

cat  $file | sort -u | httpx -probe -ip | tee -a $inputFile

while read -r host
do
  success=$(echo $host| cut -d " " -f2 | tr "[]" " ")

  if [[ $success == *"SUCCESS"* ]]; then
  ip=$(echo $host | cut -d " " -f3 | tr "[]" " " | tr -d ' ')
  orgName=$(curl -ks https://ipinfo.io/$ip | jq '.org')
  echo "$host $orgName" | tee -a $outputFile
  fi
done<$inputFile

echo -e "\nData was saved to: $(pwd)/$outputFile"
