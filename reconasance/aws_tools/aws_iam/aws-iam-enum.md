# AWS enumeration

WS Enumeration is the process of systematically discovering and gathering information about AWS resources, services, and configurations within a target environment. This reconnaissance technique involves:

- Resource Discovery: Identifying EC2 instances, S3 buckets, databases, load balancers, etc.
- Service Mapping: Discovering which AWS services are in use and how they're configured
- Permission Analysis: Understanding IAM roles, policies, and access controls
- Network Discovery: Mapping VPCs, subnets, security groups, and network topology
- Metadata Extraction: Gathering information about configurations, versions, and settings

AWS enumeration is commonly used in penetration testing, security assessments, and red team exercises to understand the attack surface and identify potential misconfigurations or vulnerabilities in cloud infrastructure.


```bash
aws configure --profile [profile]
aws sts get-caller-identity --profile [profile]
```
## IAM users
```bash
aws iam list-users --profile [profile]
aws iam list-users --query 'Users[*].UserName' --output table --profile [profile]
aws iam list-groups-for-user --user-name [user-name] --profile [profile]
aws iam list-attached-user-policies --user-name [user-name] --profile [profile]
```
## IAM Groups
```bash
aws iam list-groups --profile [profile]
aws iam get-group --group-name [group-name] --profile [profile]
aws iam list-attached-group-policies --group-name [group-name] --profile [profile]
aws iam list-group-policies --group-name [group-name] --profile [profile]
```
## IAM Roles
```bash
aws iam list-roles --profile [profile]
aws iam list-attached-role-policies --role-name [role-name] --profile [profile]
aws iam list-role-policies --role-name [ role-name] --profile [profile]
aws iam get role --rolename ec2-role --profile [profile]
aws iam list-roles --query 'Roles[?contains(RoleName, `crossaccount`) || contains(RoleName, `admin`) || contains(RoleName, `devops`)].{RoleName:RoleName,Arn:Arn}' --output table --profile [profile]
aws iam list-roles --output json | jq '.Roles[] | select(.RoleName | test("crossaccount|admin|devops"))'
echo "crossaccount-role admin-role devops-role" | xargs -n1 -I {} aws iam get-role --role-name {} --query 'Role.AssumeRolePolicyDocument.Statement[0].Principal' --output json
```
## IAM Policies
```bash
aws iam list-policies --profile [profile]
aws iam get-policy --policy-arn [policy-arn] --profile [profile]
aws iam list-policy-versions --policy-arn [policy-arn] --profile [profile]
aws iam get-policy-version --policy-arn [policy-arn] --version-id [version-id] --profile [profile]
aws iam get-user-policy --user-name [user-name] --policy-name [policy-name] --profile [profile]
aws iam get-group-policy --group-name [group-name] --policy-name [policy-name] --profile [profile]
aws iam get-role-policy --role-name [role-name] --policy-name [policy-name] --profile [profile]
```


## Privilege escalation path

```bash
aws iam list-user-policies --user-name temp-user --profile pwn
aws iam get-user-policy --user-name temp-user --policy-name test-temp-user --profile pwn
aws sts assume-role --role-arn arn:aws:iam::107513503799:role/AdminRole --role-session-name MySession
```
