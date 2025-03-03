# Check for the latest ip addresses belongs to AWS s3 service

curl https://ip-ranges.amazonaws.com/ip-ranges.json | jq -r '.prefixes[] | select(.service=="S3") | .ip_prefix'

# Run tool

$ check_ip_aws_s3.sh your_ip_address
