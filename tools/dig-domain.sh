#!/usr/bin/env bash

domain=$1
dnsName=google

selectDns(){
    case $dnsName in
        'google') dns=8.8.8.8;;
        'custom') dns=1.1.1.1;;
        'altavista') dns=2.2.2.2;;
    esac
}


domainTransfer(){
  echo -e "\n"
  echo "[+] Nameserver is set to $dnsName" |tr a-z A-Z
  echo -e "Trying domain transfer.."
  dig "@$dns" $domain axfr
}

echo -e "\n"
echo -e "--- Get Dns information ---"
dig $domain ANY +noall +answer

#More obscurely, for the present anyway, you can also poll for a host’s IPv6 address using the AAAA option.
dig $domain AAAA +short

selectDns
domainTransfer

