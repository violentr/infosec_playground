#!/usr/bin/env bash

cookie=$(cat cookie | tail -2 |cut -f 6,7)
formated="$(echo $cookie | tr " " "=")"

if [[ $formated ]]; then
 	printf "Cookie value is set to: \n"
	echo $cookie
	export COOKIE=$formated
fi

printf "\n"

while IFS='' read -r line || [[ -n "$line" ]]; do
		./scraper.py -U $line
    echo "Text read from file: $line"
done < "$1"

#./scraper.py -U $1

#cat results.txt |cut -d"/" -f 3

