# Check for the latest ip addresses belongs to AWS s3 service

curl https://ip-ranges.amazonaws.com/ip-ranges.json | jq -r '.prefixes[] | select(.service=="S3") | .ip_prefix'

# Run tool

$ check_ip_aws_s3.sh your_ip_address


# More tools
- https://github.com/initstring/cloud_enum

```bash
$ uv run cloud_enum.py -k cwl-metatech --disable-azure --disable-gcp
```


## AWS s3 enumeration

```bash
aws s3 ls s3://$bucket-name --no-sign-request
aws s3 ls s3://$bucket-name/migration-files/ . --recursive
aws s3api get-bucket-policy --bucket $bucket-name | jq -r '.Policy | fromjson'
```

Could leak contents of the bucket

- pay attention to the params in the url

https://$bucket-name.s3.amazonaws.com/?prefix=&delimiter=/
