#!/usr/bin/env bash
#
username=emp001
role=ec2-role
policy_arn="arn:aws:iam::aws:policy/ReadOnlyAccess"
group=employees

echo -e "\n[+] Current Information"
aws sts get-caller-identity --output json
#
# Users
echo -e "\n[+] Checking Users related information"
aws iam list-users --query 'Users[*].UserName' --output json
aws iam list-attached-user-policies --user-name $username  --output json
aws iam list-user-policies --user-name $username --output json # inline policy

# Groups
echo -e "\n[+] Checking Groups related information"
aws iam list-groups --query 'Groups[*].GroupName' --output json
aws iam list-group-policies --group-name $group --output json
aws iam list-attached-group-policies --group-name $group --query "AttachedPolicies[*].PolicyArn" --output json
# Policies
echo -e "\n[+] Checking Policy related information"
aws iam list-policies --scope Local --query 'Policies[*].Arn' --output json
aws iam get-policy --policy-arn "$policy_arn" --output json

# Roles
echo -e "\n[+] Checking Role related information"
aws iam list-roles --query 'Roles[*].AssumeRolePolicyDocument.Statement[0].Principal.AWS' --output json
aws iam list-role-policies --role-name $role --output json
aws iam list-attached-role-policies --role-name $role --output json
aws iam list-role-policies --role-name $role --output json
