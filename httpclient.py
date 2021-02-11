#!/usr/bin/env python3
# coding: utf-8
# Copyright 2016 Abram Hindle, https://github.com/tywtyw2002, and https://github.com/treedust
# 
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
# 
#     http://www.apache.org/licenses/LICENSE-2.0
# 
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
###################################################################################
# Copyright [2021] Haotian Qi

# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at

#     http://www.apache.org/licenses/LICENSE-2.0

# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
###################################################################################

# Do not use urllib's HTTP GET and POST mechanisms.
# Write your own HTTP GET and POST
# The point is to understand what you have to send and get experience with it

import sys
import socket
import re
# you may use urllib to encode data appropriately
# import urllib.parse
from urllib.parse import urlparse, urlencode

# GLOBAL
endl = "\r\n"
ver = "HTTP/1.1"
conn_cls = "Connection: close"



def help():
    print("httpclient.py [GET/POST] [URL]\n")

class HTTPResponse(object):
    def __init__(self, code=200, body=""):
        self.code = code
        self.body = body

class HTTPClient(object):
    #def get_host_port(self,url):

    def connect(self, host, port):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.connect((host, port))
        return None

    def get_code(self, data):
        return None

    def get_headers(self,data):
        return None

    def get_body(self, data):
        return None
    
    def sendall(self, data):
        self.socket.sendall(data.encode('utf-8'))
        
    def close(self):
        self.socket.close()

    # read everything from the socket
    def recvall(self, sock):
        buffer = bytearray()
        done = False
        while not done:
            part = sock.recv(1024)
            if (part):
                buffer.extend(part)
            else:
                done = not part
        return buffer.decode('utf-8')

    # parse scheme, host, port, path from url
    def parse_url(self, url):
        port = 80
        path = "/"
        scheme = ""
        
        o = urlparse(url)
        # split host and port
        if (o.port != None):
            port = o.port
            host = (o.netloc.split(":"))[0]
        else:            
            host = o.netloc

        #path
        if o.path != "":
            path = o.path

        # scheme
        if o.scheme == "https" or o.scheme == "http":
            scheme = o.scheme + "://" 

        return scheme, host, port, path

    def GET(self, url, args=None):        
        code = 500
        body = ""
        req_str = ""
        md ="GET"
               
        scheme, host, port, path = self.parse_url(url)
        
        # combine # GET <path> ver Host:<host>
        req_str = f'{md} {path} {ver}{endl}Host: {host}{endl}{conn_cls}{endl}{endl}'

        # do request
        try:
            self.connect(host, port)
            self.sendall(req_str)        
        except:
            print(code)
            print(body) 
            return HTTPResponse(code, body)
        buffer = self.recvall(self.socket)
        self.close()

        lines = buffer.split("\r\n")
        body = lines[-1]
        code = (lines[0].split(' '))[1]

        print(code)
        print(body)        
        
        return HTTPResponse(int(code), body)

    def POST(self, url, args=None):
        code = 500
        body = ""
        md ="POST"
        req_str = ""
        app = "Content-Type: application/x-www-form-urlencoded"
        arg_str = ""

        scheme, host, port, path = self.parse_url(url)

        #args
        if args != None:
            arg_str = urlencode(args)

        length = len(arg_str.encode('utf-8'))

        # combine # GET <path> ver Host:<host>
        req_str = f'{md} {path} {ver}{endl}Host: {host}{endl}{app}{endl}Content-Length: {length}{endl}{conn_cls}{endl}{endl}{arg_str}'
        
        # do request
        try:
            self.connect(host, port)
            self.sendall(req_str)        
        except:
            print(code)
            print(body) 
            return HTTPResponse(code, body)
        buffer = self.recvall(self.socket)
        self.close()

        lines = buffer.split("\r\n")
        body = lines[-1]
        code = (lines[0].split(' '))[1]

        # print(code)
        # print(body) 

        return HTTPResponse(int(code), body)

    def command(self, url, command="GET", args=None):
        if (command == "POST"):
            return self.POST( url, args )
        else:
            return self.GET( url, args )
    
if __name__ == "__main__":
    client = HTTPClient()
    command = "GET"
    if (len(sys.argv) <= 1):
        help()
        sys.exit(1)
    elif (len(sys.argv) == 3):
        print(client.command( sys.argv[2], sys.argv[1] ))
    else:
        print(client.command( sys.argv[1] ))

