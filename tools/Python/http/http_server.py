#!/usr/bin/env python
# Python 3

import os
from http.server import HTTPServer, BaseHTTPRequestHandler

PORT_NUMBER = 8000


class MyHandler(BaseHTTPRequestHandler):

    def do_GET(self):
        mime_type = "text/html"

        if self.path == "/":
            f, code = self.read_file('index.html')
            contents = f.read()
            self.response(mime_type, code, contents)
            f.close()
            return
        else:
            self.default_content()

    def read_file(self, filename=None):
        path = os.getcwd() + os.sep + str(filename)

        if os.path.exists(path):
            f = open(path, 'rb')
            return (f, 200)
        else:
            f = open('404.html', 'rb')
            return (f, 404)

    def default_content(self):
        # contents = bytes('Notning found here! \n', "utf8")

        f, code = self.read_file()
        self.response("text/html", code, f.read())

    def response(self, mime_type, code, contents):
        self.send_response(code)
        self.send_header("Content-type", mime_type)
        self.end_headers()
        self.wfile.write(contents)


def run():
    try:
        ip_address = ''
        config = (ip_address, PORT_NUMBER)
        server = HTTPServer(config, MyHandler)
        print("Started httpserver on ", PORT_NUMBER)
        server.serve_forever()

    except KeyboardInterrupt:
        print("Ctrrl +C received , shutting down http_server")
        server.socket.close()


if __name__ == "__main__":
    run()
