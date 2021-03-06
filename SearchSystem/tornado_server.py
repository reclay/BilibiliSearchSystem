# coding=utf-8
from tornado.wsgi import WSGIContainer
from tornado.httpserver import HTTPServer
from tornado.ioloop import IOLoop
from myflask import app
http_server = HTTPServer(WSGIContainer(app))
http_server.listen(50000)  # flask默认的端口
IOLoop.instance().start()