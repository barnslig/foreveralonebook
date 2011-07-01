#!/usr/bin/python
import daemon
from flup.server.fcgi import WSGIServer
from werkzeug.contrib.fixers import LighttpdCGIRootFix
from foreveralonebook import app

#with daemon.DaemonContext():
WSGIServer(app, bindAddress='/tmp/feabook.sock').run()
