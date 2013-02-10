#!/usr/bin/python2
from os import listdir
import sys
import BaseHTTPServer

# Some configuration
dirlist = ["/var/lib/pacman/sync", "/var/cache/pacman/pkg"]
filehash = {}
port = 9000

class MyFileObj:
    '''Object to denote a file in the paths declared above'''
    def __init__(this, path, name):
        '''Constructor'''
        this.path = path
        this.name = name
        this.fullpath = path + "/" + name
        this.mimetype = 'application/x-compressed'
    def addto(this, dictionary):
        '''Add the file to a dictionary so that it can be retrieved by name'''
        dictionary[this.name] = this

def init(x, l):
    '''Initialize the dictionary'''
    for d in l:
        for f in listdir(d):
            o = MyFileObj(d, f)
            o.addto(x)

def req(x, url):
    '''retrieve filename based on URL from dictionary'''
    try:
        return x[url.split('/')[-1]]
    except KeyError:
        return None

class PacHandler(BaseHTTPServer.BaseHTTPRequestHandler):
    '''class for BaseHTTPServer'''
    def do_HEAD(s):
        '''method called on HEAD call'''
        s.send_response(200)
        s.send_header("Content-type", "text/html")
        s.end_headers()

    def do_GET(s):
        '''method called on GET call'''
        global filehash
        try:
            instance = req(filehash, s.path)
            f = instance.fullpath
            m = instance.mimetype
            s.send_response(200)
            s.send_header("Content-type", m)
            s.end_headers()
            print "Request identified for " + f
            h = open(f, 'rb')
            s.wfile.write(h.read())
            h.close()
            print "Request for " + f + " fulfilled"
        except Exception:
            print "Bad request " + s.path + "; returning timeout (408)"
            s.send_response(408)
            s.send_header('Content-type', 'text/html')
            s.end_headers()

def main(args):
    '''main method; execution to start here'''
    global filehash
    global port
    global dirlist
    try:
        port = int(args[args.index('-p') + 1])
    except ValueError:
        pass

    print "Loading files"
    init(filehash, dirlist)
    print "Loading files done"

    httpd = BaseHTTPServer.HTTPServer(('', port), PacHandler)
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print "Interrupt received - quitting server"
    httpd.server_close()

if __name__ == '__main__':
    main(sys.argv)
