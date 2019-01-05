#!/usr/bin/env python

from bs4 import BeautifulSoup
from collections import namedtuple
import requests

TAGS = ["script", "img", "iframe"]
ParseItem = namedtuple('ParseItem', 'items tag_name attr file')
FILE = 'results.txt'
try:
    url = input("Enter a website to extract the URL's from: ")
    print("\n")

    r = requests.get(url)
    data = r.text
except Exception as e:
    print("Something went terribly wrong..")

def parse_content(content):
    str = ""
    if bool(content.items):
        message ="[+] FOUND <%s> TAG \n" % content.tag_name
        str += message
        print(message)
        for item in content.items:
            src = item.get(content.attr, "snippet")
            if src == "snippet":
                message = "%s - %s \n" % (item, src)
                str += message
                print(message);
            else:
                message = "%s - %s \n" % (content.tag_name, src)
                str += message
                print(message);
    content.file.write(str)

soup = BeautifulSoup(data, features="html5lib")
with open(FILE, 'w') as f:
    for tag in TAGS:
        data = soup.find_all(tag)
        current_tag = ParseItem(data, tag, 'src', f)
        parse_content(current_tag)
f.close
