# -*- coding: utf-8 -*-
__author__ = 'lw'
import web
import module_share
import sys
import traceback
import threading

class index:
    def GET(self):
        result = 'ok'
        try:
            data = web.input()
            do = data.do
            if do == 'init_share_name':
                t1 = threading.Thread(target=module_share.synShares, args=(u'爱情买卖',))
                t1.setDaemon(True)
                t1.start()
            elif do == 'check_share_name':
                f = open('share_name.txt')
                f.close()
        except Exception, e:
            except_str = ''
            info = sys.exc_info()
            for except_file, lineno, function, text in traceback.extract_tb(info[2]):
                except_str += except_file + ' line: ' + str(lineno) + ' in ' + function + '\n' + text + '\n'
            except_str += "** %s: %s" % info[:2]
            return except_str
        return result
    def POST(self):
        return "post, world233!"