#!/usr/bin/env bash
list="$(cat  "emails.txt")"

for email in $list; do
  ./validate_email.py $email
done
