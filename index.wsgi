# -*- coding: utf-8 -*-
import sae
import web
import os

from index import index
from llwprivate import llwprivate

urls = (
    '/index', 'index'
    '/llwprivate', 'llwprivate'
)

# def app(environ, start_response):
#     status = '200 OK'
#     response_headers = [('Content-type', 'text/plain')]
#     start_response(status, response_headers)
#     return ['Hello, world23!']
#
# application = sae.create_wsgi_app(app)


# app_root = os.path.dirname(__file__)
# templates_root = os.path.join(app_root, 'templates')
# render = web.template.render(templates_root)

app2 = web.application(urls, globals()).wsgifunc()
application = sae.create_wsgi_app(app2)
