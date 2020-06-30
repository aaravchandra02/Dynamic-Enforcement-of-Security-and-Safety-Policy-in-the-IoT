#!/usr/bin/python
from http.server import BaseHTTPRequestHandler,HTTPServer
import simplejson
import socketserver

port_num = 9090

#Dealing with incoming requests from the browser

class RequestHandler(BaseHTTPRequestHandler):
    def _set_headers(self):
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.end_headers()

    def do_GET(self):
        out = "Yes"
        self.send_response(200)
        self.send_header('Content-type','text/html')
        self.end_headers()
        self.wfile.write(out.encode(encoding='utf_8'))
        # print (out)
        return

    def do_POST(self):
        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length)
        print ("post data from client:")
        print (post_data)

        data = simplejson.loads(post_data)
        print (type(data))
        print (data["param2"]["values"][0])
        self.send_header('Content-type', 'application/json')
        if data["param2"]["values"][0]=="active":
            response = {'Permission':'Yes'}
        else:
            response = {'Permission':'No'}
        
        #xxxx = (simplejson.dumps(response), 'utf-8')
        self._set_headers()
        self.wfile.write(simplejson.dumps(response).encode('utf-8'))
try:
    server = HTTPServer(('', port_num), RequestHandler)
    print ('Started httpserver on port ' , port_num)

    server.serve_forever()

except KeyboardInterrupt:
    print ('^C received, shutting down the web server')
    server.socket.close()

