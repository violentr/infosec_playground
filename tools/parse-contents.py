#!/usr/bin/env python
import requests
from bs4 import BeautifulSoup

def get_data(url):
    response = requests.get(url)
    return BeautifulSoup(response.text, "html5lib")

def read_content(markup, tagname, parser='xml'):
    collection = []
    for i in markup.find_all(tagname):
        item = i.text if parser == 'xml' else i.get('href', '')
        collection.append(item)
    return collection

def write_file(filename, contents):
    with open(filename, 'w') as f:
        f.write("\n".join(contents))
    print("[+] results were written to %s" % filename)

url = "https://sproutsocial.com/"
filename = './results.txt'

data = get_data(url)
tagname = 'a'
parsed_data = read_content(data, tagname, 'html')
write_file(filename, parsed_data)
