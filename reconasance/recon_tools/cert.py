import ssl, sys, re, socket
from cryptography import x509
from cryptography.hazmat.backends import default_backend
from threading import Thread

search_pattern = ["worldpay"]
port = 443
socket.setdefaulttimeout(5)
filtered = False
hostname = sys.argv[1]
filename = f"{hostname}-output.txt"

def format(string):
    domain = string.split("CN=")[1]
    domain = re.sub("\)", "", domain)
    return re.sub(">", "", domain)


def grep_certificate_subject(ip_string):
    global port
    cert = ssl.get_server_certificate((ip_string, port))
    certDecoded = x509.load_pem_x509_certificate(str.encode(cert), default_backend)
    cert = format(str(certDecoded.issuer))
    subject = format(str(certDecoded.subject))
    msg = f'{ip_string} | {subject} \n'
    if filtered:
        match = re.search(search_criteria[0], subject)
        if match:
            return msg
    else:
        return msg

def run_individual_scan(hostname):
    try:
        result = grep_certificate_subject(hostname)
        print(result)
        write_tofile(result)
    except KeyboardInterrupt as e:
        print("[!] Ctrl+C detected, exiting now ..")
        sys.exit(1)
    except Exception as e:
        print(f'[!] Timeout can\'t connect to {hostname}')

def run__range_scan(hostname):
    for i in range(1, 255):
        hostname = ".".join(hostname.split(".")[:3])
        hostname = f'{hostname}.{i}'
        print("Hostname", hostname)
        run_individual_scan(hostname)
    
def write_tofile(data):
    global filename
    try:
        with open(filename, "a") as f:
            f.write(data)
    except Exception as e:
        print(e)

def process():
    global hostname
    #run_individual_scan()
    run__range_scan(hostname)

def main():
    process()

if __name__ == "__main__":
    main()
