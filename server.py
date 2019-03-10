#!/usr/bin/env python
# Reflects the requests from HTTP methods GET, POST, PUT, and DELETE

import re

from http.server import HTTPServer, SimpleHTTPRequestHandler

class RequestHandler(SimpleHTTPRequestHandler):
    
    def do_GET(self):
        request_path = self.path
        if re.search(r"^/$|(^/lib/css/.*)|(^/lib/vendor/.*)|(^/lib/javascript/.*)|(^/images/.*)|(^/html/.*)|(^/src/.*)|(^/data/.*)|(^/favicon.ico)",request_path) is not None:
            return SimpleHTTPRequestHandler.do_GET(self)
        else:
            print("\n----- Request Start ----->\n")
            print("Request path:GET")
            print("Request path:", request_path)
            print("Request headers:", self.headers)
            print("<----- Request End -----\n")
            
            self.send_response(200)
            # self.send_header("Set-Cookie", "foo=bar")
            self.end_headers()
        
    def do_POST(self):
        
        request_path = self.path
        if re.search(r"^/$|(^/lib/css/.*)|(^/lib/vendor/.*)|(^/lib/javascript/.*)|(^/images/.*)|(^/html/.*)|(^/src/.*)|(^/data/.*)|(^/favicon.ico)",request_path) is not None:
            return SimpleHTTPRequestHandler.do_GET(self)
        else:
            print("\n----- Request Start ----->\n")
            print("Request path:POST")
            print("Request path:", request_path)
            
            request_headers = self.headers
            content_length = request_headers.get('Content-Length')
            length = int(content_length) if content_length else 0
            
            print("Content Length:", length)
            print("Request headers:", request_headers)
            print("Request payload:", self.rfile.read(length))
            print("<----- Request End -----\n")
            
            self.send_response(200)
            self.end_headers()
    
    def do_PUT(self): 
        request_path = self.path
        if re.search(r"^/$|(^/lib/css/.*)|(^/lib/vendor/.*)|(^/lib/javascript/.*)|(^/images/.*)|(^/html/.*)|(^/src/.*)|(^/data/.*)|(^/favicon.ico)",request_path) is not None:
            return SimpleHTTPRequestHandler.do_GET(self)
        else:
            print("\n----- Request Start ----->\n")
            print("Request path:PUT")
            print("Request path:", request_path)
            
            request_headers = self.headers
            content_length = request_headers.get('Content-Length')
            length = int(content_length) if content_length else 0
            
            print("Content Length:", length)
            print("Request headers:", request_headers)
            print("Request payload:", self.rfile.read(length))
            print("<----- Request End -----\n")
            self.send_response(200)
            self.end_headers()
    

    def do_DELETE(self): 
        request_path = self.path
        if re.search(r"^/$|(^/lib/css/.*)|(^/lib/vendor/.*)|(^/lib/javascript/.*)|(^/images/.*)|(^/html/.*)|(^/src/.*)|(^/data/.*)|(^/favicon.ico)",request_path) is not None:
            return SimpleHTTPRequestHandler.do_GET(self)
        else:
            print("\n----- Request Start ----->\n")
            print("Request path:DELETE")
            print("Request path:", request_path)
            print("Request headers:", self.headers)
            print("<----- Request End -----\n")
            
            self.send_response(200)
            # self.send_header("Set-Cookie", "foo=bar")
            self.end_headers()

def main():
    port = 8080
    print('Listening on localhost: %s' % port)
    server = HTTPServer(('', port), RequestHandler)
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        server.server_close()
        
if __name__ == "__main__":
    main()