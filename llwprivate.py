# -*- coding: utf-8 -*-
__author__ = 'lw'
import web
import hashlib
import lxml
import time
import os
import traceback
import sys
from lxml import etree


class llwprivate:

    def __init__(self):
        self.app_root = os.path.dirname(__file__)
        self.templates_root = os.path.join(self.app_root, 'templates')
        self.render = web.template.render(self.templates_root)

    def GET(self):
        # 获取输入参数
        try:
            data = web.input()
            signature=data.signature
            timestamp=data.timestamp
            nonce=data.nonce
            echostr=data.echostr
            #自己的token
            token="llwprivate233" #这里改写你在微信公众平台里输入的token
            #字典序排序
            list=[token,timestamp,nonce]
            list.sort()
            sha1=hashlib.sha1()
            map(sha1.update,list)
            hashcode=sha1.hexdigest()
            #sha1加密算法

            #如果是来自微信的请求，则回复echostr
            if hashcode == signature:
                return echostr
            return 'not equal'
        except Exception, e:
            try:
                except_str = ''
                info = sys.exc_info()
                for except_file, lineno, function, text in traceback.extract_tb(info[2]):
                    except_str += except_file+' line: '+str(lineno)+' in '+function+'\n'+text+'\n'
                except_str += "** %s: %s" % info[:2]
                return except_str
            except Exception, e:
                return repr(e)

    def POST(self):
        try:
            str_xml = web.data() #获得post来的数据
            xml = etree.fromstring(str_xml)#进行XML解析
            content=xml.find("Content").text#获得用户所输入的内容
            msgType=xml.find("MsgType").text
            fromUser=xml.find("FromUserName").text
            toUser=xml.find("ToUserName").text
            return self.render.reply_text(fromUser,toUser,int(time.time()),u""+content)
        except Exception, e:
            try:
                except_str = ''
                info = sys.exc_info()
                for except_file, lineno, function, text in traceback.extract_tb(info[2]):
                    except_str += except_file+' line: '+str(lineno)+' in '+function+'\n'+text+'\n'
                except_str += "** %s: %s" % info[:2]
                return except_str
            except Exception, e:
                return repr(e)
