from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import *
import time

hostName = "localhost"
hostPort = 9000

class Lesserver(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.end_headers()

        parse_result = urlparse(self.path)

        print(self.client_address)
        print(self.command)
        print(self.requestline)

        print("path",parse_result.path)
        print("query",parse_result.query)

        print(parse_qs(parse_result.query))
        

    def do_POST(self):
        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.end_headers()

        parse_result = urlparse(self.path)

        print(self.client_address)
        print(self.command)
        print(self.requestline)

        print("path",parse_result.path)
        print("query",parse_result.query)

        print(parse_qs(parse_result.query))

        content_length = int(self.headers.get('content-length', 0))
        print("content-length:",content_length)
        encoded_body = self.rfile.read(content_length)
        print(type(encoded_body))
        print(encoded_body.decode('utf-8'))

myServer = HTTPServer((hostName, hostPort), Lesserver)
print(time.asctime(), "Server Starts - %s:%s" % (hostName, hostPort))

try:
    myServer.serve_forever()
except KeyboardInterrupt:
    pass

myServer.server_close()
print(time.asctime(), "Server Stops - %s:%s" % (hostName, hostPort))