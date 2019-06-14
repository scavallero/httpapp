#
# MIT License
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

import time
import sys
sys.path.append( './httpapp' )

import httpapp
from httpapp import addurl
from httpapp import addstatic


@addurl('/')
def root(p,m):
    return "Hello from Python Http Application Server"

@addurl('/postbody')
def postbody(p,m,b):
    print("Path: %s" % p)
    print("Method: %s" % m)
    print("Body: %s" % b)
    return "Post received"

@addurl('/pause')
def pause(p,m):
    time.sleep(20)
    return "Pause complete"


@addurl('/subpath/')
def pause(p,m):
    print("Path: %s" % p)
    print("Method: %s" % m)
    return "Get subpath"

@addurl('/subpath/pollo/')
def pollo(p,m):
    print("Pollo: %s" % p)
    print("Method: %s" % m)
    return "Get subpath"


addstatic("/pippo/pluto/","d:/Lorenzo")
addstatic("/pippo/","d:/Max")


httpapp.run()
