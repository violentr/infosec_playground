#/usr/bin/env bash
#Check aws s3 permissions (as authenticated user) for the bucket in all regions
if [[ $# -eq 0 ]]
then
  echo "[-]Error: Please provide hostname, example: hostname.s3.amazonaws.com"
  exit 1
else
  hostname=$1
  while read line
  do
  bucket=$(dig cname $hostname +short)
  bucket_name=$(echo $bucket | sed 's/\.$//')
  echo "Checking permissions for s3://$bucket_name --region $line"
  aws s3 ls s3://$bucket_name --no-sign-request --region $line
  done < aws-regions.txt
fi
