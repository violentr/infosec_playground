#!/usr/bin/env python

#Python 2.7
#Method 1:
# EDIT cookie.txt and put correct session cookie
# SCRIPT:  ./script.sh

# Method 2:
# EXAMPLE: ./scraper.py -H '{"Cookie": "_session=c241UXVDdDFGU2NhSmo5c3"}'

import sys
import json
import os
from collections import namedtuple

DEPENDENCIES = ["bs4", "requests", "html5lib"]
REQUIRED = { k:v for k, v in zip( DEPENDENCIES, DEPENDENCIES) }

TAGS = ["script", "img", "iframe", "link", "frame", "iframe"]
ParseItem = namedtuple('ParseItem', 'items tag_name attr')
FILE = 'results.txt'

try:
    from bs4 import BeautifulSoup
    import requests
    from options_parser import args
    import html5lib
except ImportError as e:
    lib = e.message.split(' ')[-1]
    sys.exit('[!] Error package missing, try pip install %s' % (REQUIRED[lib]))


class HandleRequest():
    def __init__(self, url):
        self.url = url

    def start(self):
        try:
            self.url or sys.exit("[!] Error - Url should be specified, try again..")
            print("\n")
            headers = args.headers or self.__read_cookie()
            response = requests.get(self.url, headers=self.__parse_json(headers) )
            print("Headers: %s \n\n" % response.headers)
            return response
        except Exception as e:
            print("[!] Error %s" % e.message)
            sys.exit("[!] Something went terribly wrong..")

    def __read_cookie(self):
        cookie = os.environ.get("COOKIE", None)
        return '{"Cookie": "%s"}' % cookie

    def __parse_json(self, string):
        if string:
            return json.loads(string)
        return {}

class HandleResponse():

    def __init__(self, html, url, options):
        self.html = html
        self.url = url
        self.options = options

    def to_file(self, file_):
        with open(file_, 'w') as f:
            message = "[+] Processing current url %s \n\n" % url
            f.write(message)
            f.write(self.options)
            for tag in TAGS:
                data = self.html.find_all(tag)
                current_tag = ParseItem(data, tag, 'src')
                f.write(self.__parse_content(current_tag))
        return f.close

    def __parse_content(self, content):
        str = "\n"
        if bool(content.items):
            message ="[+] FOUND <%s> TAG \n" % content.tag_name
            str += message
            print(message)
            for item in content.items:
                src = item.get(content.attr, "snippet")
                if src == "snippet":
                    message = "%s - %s \n\n" % (item, src)
                    str += message
                    print(message)
                else:
                    message = "%s - %s \n\n" % (content.tag_name, src)
                    str += message
                    print(message)
        return str


url =  args.url or raw_input("Enter a website to extract the URL's from:")
request = HandleRequest(url)

data = request.start()
url = request.url
domain_name = url.split("/")[2]

if not os.path.isdir(domain_name):
    os.mkdir(domain_name)

soup = BeautifulSoup(data.text, features="html5lib")
file_name = url.split("/")[-1]

FILE = file_name or "index.txt"
path = "./%s/%s" % (domain_name, FILE)

HandleResponse(soup, url, "Headers: %s \n\n" % data.headers).to_file(path)
print("[+] Output was saved to file: %s" % path)
