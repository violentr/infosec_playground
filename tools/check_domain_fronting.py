import socket
import requests
import sys
from requests.packages.urllib3.exceptions import InsecureRequestWarning
from requests.exceptions import SSLError

# Drop SSL Cert verification
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

# Usage:
# python check_domain_fronting your_input_file | tee -a output.txt
# cat output.txt | grep \[+\]
#
def resolve_host(domain):
    try:
        ip_address = socket.gethostbyname(domain)
        print(f"Domain '{domain}' resolves to IP: {ip_address}")
        return True
    except socket.gaierror:
        print(f"Domain '{domain}' could not be resolved.")
        return False

def https_server(domain):
    try:
        response = requests.get(f"https://{domain}", timeout=5, verify=False)
        if response.status_code == 200:
            print(f"Domain '{domain}' supports HTTPS.")
            return True
        else:
            print(f"Domain '{domain}' returned status code: {response.status_code}")
            return  True
    except SSLError as e:
        print(f"SSL certificate validation error occurred: {e.response}")
        return False
    except requests.exceptions.RequestException as e:
        print(f"HTTPS request failed for domain '{domain}': {e.response}")
        return False

def check_domain_fronting(domain):
    if not (resolve_host(domain)):
        return False
    elif (https_server(domain)):
        try:
            headers = {'Host': 'example.com'}
            response = requests.get(f"https://{domain}", headers=headers, timeout=5, verify=False)
            if response.status_code == 200:
                print(f"Domain '{domain}' allows different host headers.")
                return True
            else:
                print(f"Domain '{domain}' returned status code: {response.status_code} for different host header.")
                return False 
        except requests.exceptions.RequestException as e:
            print(f"Request failed for domain '{domain}' with different host header: {e}")
            return False
    else:
        print("Host {0} doesn't support HTTPs".format(domain))

def main():
    file=sys.argv[1]
    if (file) :
        try:
            with open(file) as f:
                lines = f.readlines() 
                for line in lines:
                    domain = line.strip()
                    if check_domain_fronting(domain):
                        print(f"[+] Domain '{domain}' could potentially be used for domain fronting. \n")
                    else:
                        print(f"[-] Domain '{domain}' cannot be used for domain fronting.\n")
        except KeyboardInterrupt as e:
            print("\nCtrl+C detected, stopping the program")
        except FileNotFoundError as e:
            print("[-] File was not found '{0}' !".format(e.filename))
    else:
        print("Please provide input file!")

main()
