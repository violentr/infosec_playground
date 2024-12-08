import dns.resolver
import socket
import sys
import whois
import requests

def get_ptr_records(domain_name):
    try:
        a_records = dns.resolver.resolve(domain_name, 'A')
        
        print("\nReverse DNS [PTR Records]:")
        print("-" * 50)
        
        for record in a_records:
            ip = str(record)
            # Convert IP to reverse pointer format
            reversed_ip = '.'.join(reversed(ip.split('.'))) + '.in-addr.arpa'
            
            try:
                ptr_records = dns.resolver.resolve(reversed_ip, 'PTR')
                print(f"\nIP Address {ip} resolves to:")
                for ptr in ptr_records:
                    print(f"  {ptr}")
            except dns.resolver.NXDOMAIN:
                print(f"  No PTR record found for {ip}")
            except dns.resolver.NoAnswer:
                print(f"  No PTR record found for {ip}")
            except Exception as e:
                print(f"[!]  Error getting PTR record for {ip}: {str(e)}")
                
    except dns.resolver.NXDOMAIN:
        print("[!] Error: Domain does not exist")
    except dns.resolver.NoAnswer:
        print("[!] Error: No A records found")
    except Exception as e:
        print(f"[!] Error: {str(e)}")

def get_ip(domain_name):
    try:
        return socket.gethostbyname(domain_name)
    except socket.gaierror:
        print("[!] Error: Could not resolve IP address")


def get_reverse_ip_lookup(domain_name):
    try:
        ip_address = get_ip(domain_name)
        
        print(f"\nReverse IP Lookup (domains on same IP {ip_address}):")
        print("-" * 50)
        
        url = f"https://api.hackertarget.com/reverseiplookup/?q={ip_address}"
        response = requests.get(url)
        
        if response.status_code == 200:
            domains = response.text.split('\n')
            if len(domains) > 0 and not response.text.startswith('error'):
                for domain in domains:
                    if domain.strip():
                        print(f"  {domain.strip()}")
            else:
                print("[-]  No other domains found or daily lookup limit reached")
        else:
            print("[-]  Failed to perform reverse IP lookup")
            
    except Exception as e:
        print(f"[!] Error performing reverse IP lookup: {str(e)}")

def get_dns_info(domain_name):
    try:
        a_records = dns.resolver.resolve(domain_name, 'A')
        print(f"\nDomain Information for: {domain_name}")
        print("-" * 50)
        print("IP Addresses:")
        for record in a_records:
            print(f"  {record}")

        try:
            cname_records = dns.resolver.resolve(domain_name, 'CNAME')
            print("\nCNAME Records:")
            for record in cname_records:
                print(f"  {domain_name} is an alias for {record.target}")
        except dns.resolver.NoAnswer:
            print("\nNo CNAME records found (this is normal for root domains)")

        ns_records = dns.resolver.resolve(domain_name, 'NS')
        print("\nNameservers:")
        for record in ns_records:
            print(f"  {record}")

        try:
            mx_records = dns.resolver.resolve(domain_name, 'MX')
            print("\nMail Servers:")
            for record in mx_records:
                print(f"  Priority: {record.preference}, Server: {record.exchange}")
        except dns.resolver.NoAnswer:
            print("\nNo mail servers found")


        try:
            txt_records = dns.resolver.resolve(domain_name, 'TXT')
            print("\nTXT Records:")
            for record in txt_records:
                print(f"  {record}")
        except dns.resolver.NoAnswer:
            print("\nNo TXT records found")


    except dns.resolver.NXDOMAIN:
        print(f"[!] Error: Domain {domain_name} does not exist")
    except dns.resolver.NoAnswer:
        print(f"[!] Error: No DNS records found for {domain_name}")
    except Exception as e:
        print(f"[!] Error: {str(e)}")

def get_ip_info(domain_name):
        try:
            print(f"\nIP Information:")
            get_ptr_records(domain_name)
        except socket.herror:
            print("Reverse DNS: Not available")
            
        except socket.gaierror:
            print("[!] Error: Could not resolve IP address")

def main():
    domain_name = sys.argv[1]
    get_reverse_ip_lookup(domain_name)
    get_dns_info(domain_name)
    get_ip_info(domain_name)

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python domain_whois.py <domain_name>")
    main() 
