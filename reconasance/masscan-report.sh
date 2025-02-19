#!/usr/bin/env bash
# Run this script after running masscan.sh script
# 
echo -e "Generating report from output_4_ files \n"

output_file=port_scanning_report.txt

for file in $(ls | grep "output_4" )
do
  cat "$file" | cut -d " " -f3- | tee -a $output_file
done
