#!/usr/bin/env bash
# Enumerate existing users with rpcclient
# when user exists output should be like bob S-1-22-1-1001 (User: 1)

users_file=$1
ip=$2

if [ $# -eq 0 ]
then
  echo -e "[-] usage: $0 users.txt ip_address"
  exit 1
fi

for u in $(cat $user_file);
  do rpcclient -U "" $ip -N --command="lookupnames $u"
done |grep "User: 1"
