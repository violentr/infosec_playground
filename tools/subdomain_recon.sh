#!/usr/bin/env bash
#Great recon tool to check for subdomains

domain=$1
filename="$domain"_recon.txt
start_time="$(date +%s)"

echo -e "[+] Scanning $domain please wait ...\n "

curl -s "https://dns.bufferover.run/dns?q=$domain" | jq -r .FDNS_A[]|cut -d',' -f2|sort -u >> $filename
echo -e "Step Bufferover.run completed"

curl -s "http://web.archive.org/cdx/search/cdx?url=*."$domain"/*&output=text&fl=original&collapse=urlkey" |sort| sed -e 's_https*://__' -e "s/\/.*//" -e 's/:.*//' -e 's/^www\.//' | uniq >> $filename
echo -e "Step web_archieve completed"

curl -s "https://certspotter.com/api/v0/certs?domain="$domain | jq '.[].dns_names[]' | sed 's/\"//g' | sed 's/\*\.//g' | sort -u | grep $domain >> $filename
echo -e "Step certspotter_com completed \n"

#very slow need to wait some time
curl -s  -X POST --data "url=$domain&Submit1=Submit" https://suip.biz/?act=amass | grep $domain | cut -d ">" -f 2 | awk 'NF' | uniq >> $filename
echo -e "Step suip_biz completed\n"

cat $filename |sort |uniq | tee $filename

results=$(cat $filename |wc -l)
echo -e "\n[+] Scan completed, it took $(( $(date +%s) - start_time )) seconds"
echo -e "[+] Found $results uniq domains"
echo -e "[+] Search results were saved to $(pwd)/$filename"
