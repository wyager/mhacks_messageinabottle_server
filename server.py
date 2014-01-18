import http
from http import server
PORT = 8005


class CustomHandler(server.BaseHTTPRequestHandler):
    def do_GET(self):
        #Sample values in self for URL: http://localhost:8080/jsxmlrpc-0.3/
        #self.path  '/jsxmlrpc-0.3/'
        #self.raw_requestline   'GET /jsxmlrpc-0.3/ HTTP/1.1rn'
        #self.client_address    ('127.0.0.1', 3727)
        self.send_response(200)
        self.send_header('Content-type','text/html')
        self.end_headers()
        if self.path.startswith('/check/'):#=='/move':
            self.wfile.write(b"{\"exists\": false}")
        else:
            print("invalid url")
            self.wfile.write(b"Invalid URL")



        

httpd = server.HTTPServer(('', 8005), CustomHandler)
print("serving at port", PORT)
httpd.serve_forever()
