#!/usr/bin/env bash

# Check if ip address belongs to a list of ip addresses for AWS S3 buckets.

input=$1
input_file=aws_s3_buckets_ips.txt
output_file=aws_s3_output.txt

run_tool(){
    while read -r line
    do
    	echo "Current IP range: $line"
    	output="$(./check_ip_aws_s3.py $input  $line | grep 'The IP address')";
    	if [ ! -z "$output" ] ;then
            echo "The IP address, $input, is associated with an AWS S3 bucket"
    		echo "$output" | tee -a $output_file
            break
    	fi
    done<$input_file
}

echo "Input: $input"
if [ $# -eq 0 ]
then
   echo -e "[-] Missing IP address"
else
  run_tool
fi

