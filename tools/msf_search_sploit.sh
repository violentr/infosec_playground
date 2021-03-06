# This script will help you to automate search for the exploit
# Run it and choose option 1 for manual input or 3 to use default
# script settings. When information is collected about the host.
# It will be saved to the file, use this file as input to
# check and validate that exploit exists. This script uses
# kali linux tool - searchsploit
# Results of findings will be saved to the file
#
#!/usr/bin/env bash
default_settings=false

proj_dir="msf_check"
proj_path="$(pwd)/$proj_dir"


cleanup(){
  [ -d $proj_path ] && echo "[+] Cleaning old results" && $(rm -rf $proj_path)
}

if [ ! -d $proj_path ]; then
  mkdir -p $proj_path
  echo -e "[+] Project directory created: $proj_path"
  echo -e "[+] Current working dir set to $proj_path"
  cd $proj_path
 else
   cd $proj_path
   echo -e "[+] Your current project has these files\n"
   for i in $(ls -A)
   do
     echo -e "\t $i"
   done
fi

nmap_scan(){
  #nmap -Pn --top-ports 1000 -sU --stats-every 3m --max-retries 1 -T3 $ip_address2scan | tee $result
  #nmap -nvv -Pn -sSV -p 22,80,111,139,443,1024 --version-intensity 9 -A $ip_address2scan | tee $result

  nmap -T4 -p- -sV -vvv $ip_address2scan | tee "$result"
}

set_defaults(){
  input="$proj_path/working_copy.txt"
  output="$proj_path/output_file.txt"
  ip_address2scan="172.16.122.176"
  result="$proj_path/scan_result.txt"

  default_settings=true
  echo -e "\n [+] Default settings were set!"
}

scan_ip(){
  if [ $default_settings = false ]; then
    read -p "[+] IP to scan: " ip_address2scan
    read -p "[+] Save results to file:  " result
    result=$(pwd)/$result
  fi
  nmap_scan
  echo -e "\n[+] Results were saved to: $result file"
  #cat $result | awk -F "{print $2}" | tee $result
}

search_vuln_file(){
  if [ $default_settings = false ]; then
    read -p "[+] Please provide your input file: " input
    read -p "[+] Please provide your output file: " output
    output=$(pwd)/$output
    input=$(pwd)/$input
  fi

  while IFS= read -r line
  do
    echo "Checking exploit for: $line"
    length="$(searchsploit -w $line | wc -l)"
    if (( $length > 4 ));then
      echo -e "\n[+] Result for searching exploit: $line\n" | tee -a $output
      searchsploit -t --color -w $line | tee -a $output
    fi
  done < "$input"
  echo -e "\n [+] Oputput of vuln check was saved to : $output file"
}


echo -e "\n Please enter your choice: "
options=("Scan IP address" "Check vulns" "Set defaults" "Clean old results" "Quit")
select opt in "${options[@]}"
do
   case $opt in
       "Scan IP address")
           echo -e "\nYou chose $REPLY, scan individual ip address:"
           scan_ip
           exit
           ;;
       "Check vulns")
           echo -e "\nYou chose $REPLY, search for vulnerabilities"
           search_vuln_file
           ;;
       "Set defaults")
           echo -e "\nYou chose $REPLY"
           set_defaults
           ;;
       "Clean old results")
           echo -e "\nYou chose $REPLY, old results will be deleted"
           cleanup
           exit
           ;;
       "Quit")
           cd ..
           break
           ;;
       *) echo -e l"\n Invalid option $REPLY";;
   esac
done

