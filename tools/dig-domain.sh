#!/usr/bin/env bash

domain=$1
dnsName=google
googleMaps=https://www.google.com/maps
hackerTargetApi=https://api.hackertarget.com/geoip/?q

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

getGeoLocation(){
  printf "\n"
  echo -e "GEO ip location: \n"
  curl $hackerTargetApi=$domain |tee output.txt
  coordinates=($(cat output.txt | tail -2 | awk {'print $2'} | cut -d':' -f1))
  gps="$googleMaps/@${coordinates[0]},${coordinates[1]},10z"
  printf "\n"
}


if [ $# -eq 0 ]
  then
    echo "No arguments supplied"
    echo "usage: ./dig-domain your_domain"
  else
    echo "Supplied Param: $1"
    echo -e "\n"
    echo -e "--- Get Dns information ---"
    dig $domain ANY +noall +answer

    #More obscurely, for the present anyway, you can also poll for a host’s IPv6 address using the AAAA option.
    dig $domain AAAA +short

    selectDns
    domainTransfer
    getGeoLocation

    echo "Opening Google maps with defined coordinates"
    open /Applications/Google\ Chrome.app $gps
    printf "\n"
fi
