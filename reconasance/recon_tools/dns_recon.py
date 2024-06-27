import sys
import urllib.parse
import dns.resolver
import requests

from requests.packages.urllib3.exceptions import InsecureRequestWarning
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

"""
How to run script (brute mode):
while read -r line;do echo -e "https://$line"; python dns_recon.py https://$line;echo -e "\n";done<subfinder-worldpay_com.txt
"""
filename = "dns_recon_output.txt"

DNS_SERVERS = ['8.8.8.8']

AKAMAI_SERVERS = [
'104.94.222.123', '104.94.222.124', '104.94.222.148', '104.94.222.149', '107.162.133.46',
'23.48.165.132', '23.48.165.133', '23.48.165.134', '23.48.165.135', '23.48.165.136', '23.48.165.137',
'23.48.165.138', '23.48.165.139', '23.48.165.140', '23.48.165.141', '23.48.165.142', '23.48.165.143',
'23.48.165.144', '23.48.165.145', '23.48.165.146', '23.48.165.147', '23.48.165.148', '23.48.165.149',
'23.48.165.150', '23.48.165.151', '23.48.165.152', '23.48.165.153', '23.48.165.154', '23.48.165.155',
'23.48.165.156', '23.48.165.157', '23.48.165.158', '23.48.165.159', '23.48.165.160', '23.48.165.161',
'23.48.165.162', '23.48.165.163'
]

CLOUDFLARE_SERVERS = [
'104.16.10.2', '104.16.11.2', '104.16.131.29', '104.16.146.231', '104.16.147.231',
'104.16.153.82', '104.16.179.78', '104.16.180.238', '104.16.181.238', '104.16.204.249', '104.16.205.249',
'104.16.230.137', '104.16.231.137', '104.16.50.20', '104.16.51.20', '104.16.87.94', '104.17.155.102',
'104.17.156.102', '104.17.182.24', '104.17.183.24', '104.17.231.5', '104.17.232.5', '104.17.232.59',
'104.17.242.24', '104.17.243.24', '104.17.49.5', '104.17.50.5', '104.17.70.206', '104.17.71.206', '104.17.72.206',
'104.17.73.206', '104.17.74.206', '104.17.85.112', '104.17.86.112', '104.18.119.21', '104.18.132.33', '104.18.133.33',
'104.18.157.82', '104.18.158.82', '104.18.165.15', '104.18.185.69', '104.18.186.69', '104.18.217.235', '104.18.218.235',
'104.18.218.81', '104.18.24.129', '104.18.25.129', '104.18.255.3', '104.18.33.174', '104.18.33.211', '104.18.34.105',
'104.18.34.21', '104.18.34.4', '104.18.35.132', '104.18.35.28', '104.18.35.80', '104.18.36.21', '104.18.36.68',
'104.18.36.97', '104.18.37.111', '104.18.37.129', '104.18.37.247', '104.18.38.137', '104.18.38.177', '104.18.39.148',
'104.18.39.199', '104.18.39.22', '104.18.39.26', '104.18.39.51', '104.18.39.53', '104.18.39.90', '104.18.40.110',
'104.18.40.36', '104.18.41.160', '104.18.41.182', '104.18.41.4', '104.18.41.63', '104.18.42.153', '104.18.42.4',
'104.18.42.70', '104.18.43.129', '104.18.43.233', '104.18.43.251', '104.18.64.4', '104.19.156.81', '104.19.157.81',
'104.19.209.22', '104.19.209.84', '104.19.210.22', '104.19.210.84', '104.19.222.7', '104.19.223.7', '162.159.152.22',
'162.159.153.242', '172.64.144.127', '172.64.144.23', '172.64.144.5', '172.64.145.103', '172.64.145.186', '172.64.145.252',
'172.64.146.193', '172.64.146.252', '172.64.146.74', '172.64.146.96', '172.64.147.146', '172.64.147.220', '172.64.148.108',
'172.64.148.166', '172.64.148.203', '172.64.148.205', '172.64.148.230', '172.64.148.234', '172.64.148.57', '172.64.149.119',
'172.64.149.79', '172.64.150.127', '172.64.150.145', '172.64.150.9', '172.64.151.159', '172.64.151.188', '172.64.151.235',
'172.64.152.124', '172.64.152.176', '172.64.152.228', '172.64.153.151', '172.64.153.235', '172.64.153.252', '172.64.154.45',
'172.64.154.82'
]

def write_tofile(data):
    global filename
    try:
        with open(filename, "a") as f:
            f.write(data)
    except Exception as e:
        print(f"[!] {e}")

def make_request(url):
    try:
        r = requests.get(url, verify=False, timeout=5)
        if r.ok:
            return r
        else:
            return r
    except requests.exceptions.ConnectionError as e:
        print(f"[!] Request: No response")
    except Exception as e:
        print(f"[!] Request: Error {e}")
    
def identify_by_ip(ip_string):
    if ip_string in AKAMAI_SERVERS:
        return "AKAMAI IP"
    elif ip_string in CLOUDFLARE_SERVERS:
        return "CLOUDFLARE IP"
    else:
        return "Not behind AKAMAI or CLOUDFLARE" 

def process():
    try:
        res = dns.resolver.Resolver(configure=False)
        res.nameservers = DNS_SERVERS
        url = sys.argv[1]
        parsed_url = urllib.parse.urlparse(url)
        hostname = parsed_url.hostname
        q = res.resolve(hostname, "A")
    
        for rdata in q:
            print(f"{rdata.address} | {hostname} | {identify_by_ip(rdata.address)}")
            if not rdata.address in AKAMAI_SERVERS and not rdata.address in CLOUDFLARE_SERVERS:
                response = make_request(url)
                response = response.status_code if hasattr(response, "status_code") else "No response"
                data = f"{url} | {rdata.address} | {response} \n"
                write_tofile(data)
    
    except dns.resolver.NXDOMAIN:
        print(f"[!] DNS: [{hostname}] IP was not found")
    except dns.resolver.LifetimeTimeout as e:
        print(f"[!] DNS: [{hostname} ]Error {e}")
    except (dns.resolver.NoAnswer, dns.resolver.NoNameservers) as e:
        print(f"[!] DNS: [{hostname}] No answer ")
   
def main():
    process()

if __name__ == "__main__":
    main()
