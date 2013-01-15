#!/usr/bin/env python
from flup.server.fcgi import WSGIServer
from wgm_search import app

if __name__ == '__main__':
    WSGIServer(app).run()

