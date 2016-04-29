import sae
import web
import lxml
import time
import os
from lxml import etree

def app(environ, start_response):
    status = '200 OK'
    response_headers = [('Content-type', 'text/plain')]
    start_response(status, response_headers)
    return ['Hello, world2!']

application = sae.create_wsgi_app(app)