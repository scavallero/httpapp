#!/usr/bin/env python
# httpapp
#
# MIT Lcense
#
# Copyright (c) 2019 Salvatore Cavallero
# 
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:

# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.

# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.


import sys

if sys.version_info[0] >= 3:
    from http.server import BaseHTTPRequestHandler,HTTPServer
else:
    from BaseHTTPServer import BaseHTTPRequestHandler,HTTPServer
    
import inspect
import logging
import logging.handlers

# Callback dicrionary

urlf={}
errorf=None

# Logger
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
handler_stream = logging.StreamHandler()
formatter = logging.Formatter('*** %(asctime)s %(levelname)-8s %(message)s')
handler_stream.setFormatter(formatter)
logger.addHandler(handler_stream)

def addurl(path):
    def decorator(f):
        global urlf
        urlf[path]=f
        if path[-1] == '/' and path != '/':
            urlf[path[:-1]]=f
        return f
    return decorator

def error_default(path,command):
    return '{"status":"error","value":"undefined url %s","methd":"%s"}' % (path,command)

def log_default(format, *args):
    logger.info(format % args)

class handler_class(BaseHTTPRequestHandler):
    def _set_headers(self,value):
        self.send_response(value)
        self.send_header('Content-type', 'application/json')
        self.end_headers()

    def log_message(self, format, *args):
        log_default(format,*args)
        
    def do_GET(self):
        global urlf
        global errorf
        
        if self.path in urlf.keys():
            self._set_headers(200)
            a = len(inspect.getargspec(urlf[self.path]).args)
            if a == 1:
                self.wfile.write(urlf[self.path](self.path).encode())
            elif a == 2:
                self.wfile.write(urlf[self.path](self.path,self.command).encode())
            elif a == 3:
                self.wfile.write(urlf[self.path](self.path,self.command,None).encode())
            return
        else:
            k = self.path.rfind('/')
            subpath = self.path[:k+1]
            while subpath != '/':
                if subpath in urlf.keys():
                    self._set_headers(200)
                    a = len(inspect.getargspec(urlf[subpath]).args)
                    if a == 1:
                        self.wfile.write(urlf[subpath](self.path).encode())
                    elif a == 2:
                        self.wfile.write(urlf[subpath](self.path,self.command).encode())
                    elif a == 3:
                        self.wfile.write(urlf[subpath](self.path,self.command,None).encode())
                    return
                else:
                    k = subpath[:-1].rfind('/')
                    subpath = subpath[:k+1]

        self._set_headers(400)
        self.wfile.write(errorf(self.path,self.command).encode())
        
    def do_POST(self):
        global urlf
        global errorf

        content_len = int(self.headers.get('content-length', 0))
        post_body = self.rfile.read(content_len)

        if self.path in urlf.keys():
            self._set_headers(200)
            a = len(inspect.getargspec(urlf[self.path]).args)
            if a == 1:
                self.wfile.write(urlf[self.path](self.path).encode())
            elif a == 2:
                self.wfile.write(urlf[self.path](self.path,self.command).encode())
            elif a == 3:
                self.wfile.write(urlf[self.path](self.path,self.command,post_body).encode())
            return
        else:
            k = self.path.rfind('/')
            subpath = self.path[:k+1]
            while subpath != '/':
                if subpath in urlf.keys():
                    self._set_headers(200)
                    a = len(inspect.getargspec(urlf[subpath]).args)
                    if a == 1:
                        self.wfile.write(urlf[subpath](self.path).encode())
                    elif a == 2:
                        self.wfile.write(urlf[subpath](self.path,self.command).encode())
                    elif a == 3:
                        self.wfile.write(urlf[subpath](self.path,self.command,post_body).encode())
                    return
                else:
                    k = subpath[:-1].rfind('/')
                    subpath = subpath[:k+1]

        self._set_headers(400)
        self.wfile.write(errorf(self.path,self.command).encode())
        
def run(port=8080,error_handler=error_default,log_handler=None):
    global errorf
    global logger
    errorf = error_handler
    server_address = ('', port)
    if log_handler is not None:
        logger = log_handler
    httpd = HTTPServer(server_address, handler_class)
    logger.info("Httpapp service started on port %d" % port)
    httpd.serve_forever()


if __name__ == "__main__":

    @addurl('/')
    def root(p,m):
        return "Hello from Python Http Application Server"

    run()






