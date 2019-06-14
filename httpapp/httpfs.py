# httpfs
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

import os

fs={}

def add(path,staticdir):
    global fs
    if os.path.isdir(staticdir):
        fs[path]=staticdir
        return True
    else:
        return False

def check(path):

    k = path.rfind('/')
    subpath = path[:k+1]
    while subpath != '/':
        if subpath in fs.keys():
            return (subpath,path[k+1:])
        else:
            k = subpath[:-1].rfind('/')
            subpath = subpath[:k+1]

    print("None,None")
    return None,None


def get(path):
    subpath,localpath = check(path)
    if localpath == "":
        localpath="index.html"
    filename = fs[subpath]+"/"+localpath
    if os.path.isfile(filename):
        with open(filename,"rb") as f:
            return f.read()
    else:
        return None

        
    
