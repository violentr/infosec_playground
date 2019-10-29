#!/usr/bin/env python

import requests
import sys
from bs4 import BeautifulSoup
import os

requests.packages.urllib3.disable_warnings()
url = os.environ["URL"]
output = "email_users.txt"
email = sys.argv[1] or "user@email.com"


def setup():
    global email

    proxies = {
            "http": "http://127.0.0.1:8080",
            "https": "http://127.0.0.1:8080",
            }

    params = "lang=en&email=%s" % email

    headers = {
        'Content-Type': 'application/x-www-form-urlencoded',
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.120 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3',
        'Referer': 'https://mailtester.com/index.php'
        }
    return [params, headers, proxies]


def get_data():
    global url
    params, headers, proxies = setup()
    return requests.post(url, verify=False, data=params, headers=headers, proxies=proxies)


def process():
    global output, email

    response = get_data()
    html = BeautifulSoup(response.text, "html5lib")

    with open(output, 'w') as f:
        for i in html.find_all('tr'):
            text = i.text.strip()
            if len(text) > 0:
                f.write(text)
        print("email %s - %s" % (email, text))

process()
