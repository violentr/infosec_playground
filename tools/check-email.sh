#!/bin/bash

filename=$1
output_file="./legit-emails.txt"

handle_file(){
  if [ -e "$output_file" ]; then
    `rm $output_file`
    echo "*****************************************************"
    echo " Previous version of '$output_file' was removed "
    echo "*****************************************************"
  fi
}

IFS=$'\n'
handle_file

for email_domain in `cat $filename`
  do
    domain=`echo $email_domain |cut -d"@" -f2`
    check_result=`dig MX $domain | grep "^[^;].*MX | wc -l`
    if (( $check_result > 0 )); then
      #this is probably legit email
      echo "$email_domain" | tee -a $output_file
    fi
  done

echo -e " \t *************"
echo -e " \t  Completed ! "
echo -e " \t *************"

exit 0
