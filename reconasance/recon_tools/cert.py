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
    domain = string.split("=")[1]
    domain = re.sub("\)", "", domain)
    return re.sub(">", "", domain)


def run_scan(ip_string):
    global port
    cert = ssl.get_server_certificate((ip_string, port))
    certDecoded = x509.load_pem_x509_certificate(str.encode(cert), default_backend)
    cert = format(str(certDecoded.issuer))
    subject = format(str(certDecoded.subject))
    msg = f'{hostname} | {subject} \n'
    if filtered:
        match = re.search(search_criteria[0], subject)
        if match:
            return msg
    else:
        return msg

def process():
    global hostname
    for i in range(1, 255):
        try:
            hostname = ".".join(hostname.split(".")[:3])
            hostname = f'{hostname}.{i}'
            result = run_scan(hostname)
            print(result)
            write_tofile(result)
        except KeyboardInterrupt as e:
            print("[!] Ctrl+C detected, exiting now ..")
            sys.exit(1)
        except Exception as e:
            print(f'[!] Timeout can\'t connect to {hostname}')
    
def write_tofile(data):
    global filename
    try:
        with open(filename, "a") as f:
            f.write(data)
    except Exception as e:
        print(e)


def main():
    data = process()
    write_tofile(data)


if __name__ == "__main__":
    main()
