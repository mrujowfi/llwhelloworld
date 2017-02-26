# -*- coding: utf-8 -*-
__author__ = 'lw'
import web
import module_share

class index:
    def GET(self):
        result = 'ok'
        try:
            data = web.input()
            do = data.do
            if do == 'init_share_name':
                module_share.synShares(b_save_file=True)
            elif do == 'check_share_name':
                f = open('share_name.txt')
                f.close()
        except Exception, e:
            result = 'exception'
        return result
    def POST(self):
        return "post, world233!"