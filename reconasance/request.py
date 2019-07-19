#!/usr/bin/env python3
import requests
import os
from colorama import Fore, Back, Style
urlib3 = requests.packages.urllib3

urlib3.disable_warnings(urlib3.exceptions.InsecureRequestWarning)
proxies = {'http': 'http://127.0.0.1:8080/', 'https': 'https://127.0.0.1:8080/'}

os.system('clear')

def format_text(title, item):
    cr = '\r\n'
    decor = 20 * "*"
    section_break = "%s %s %s" % (cr, decor, cr)
    item = str(item)
    message = (Style.BRIGHT, Fore.RED, title,
            Fore.RESET, section_break, item,
            section_break)
    text = "%s %s %s %s %s %s %s" % message
    return text

url = "https://www.facebook.com"
headers = {'User-agent': 'Mozilla/5.0'}

r = requests.get(url, headers=headers, verify=False, proxies=proxies)
print(format_text('status_code', r.status_code))
print(format_text('headers', r.headers))
print(format_text('cookies', r.cookies))
print(format_text('text', r.text))
