__author__ = 'lw'
import web

class index:
    def GET(self):
        return "get, world!"
    def POST(self):
        return "post, world!"