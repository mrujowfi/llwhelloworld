# -*- coding: utf-8 -*-
__author__ = 'lw'
import web

class index:
    def GET(self):
        return "get, world23!"
    def POST(self):
        return "post, world23!"