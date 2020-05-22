#!/usr/bin/env bash

input=$1
outputFile="output-$1"

function readFile(){
  while IFS= read -r line
  do
    echo "Resolving: $line"
    output=$(dig +short $line)
    if [ -z "$output" ]
    then
      echo "N/A"
    else
      echo -e "$line --> $output\n" | tee -a $outputFile
    fi
    echo -e "\n"
  done < "$input"
}

if [ $# -eq 0 ]
then
  echo "[-] Input file is missing"
else
  [[ -f $outputFile ]] && rm $outputFile && echo -e "[+] Delete previous results\n"
  readFile
  [[ -f $outputFile ]] && echo -e "[+] Output was saved to $outputFile"
fi
