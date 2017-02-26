# -*- coding: utf-8 -*-
__author__ = 'lw'
import web
import hashlib
import lxml
import random
import time
import os
import traceback
import sys
from lxml import etree
import module_share
import module_share_kelly


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
        lbg = ''
        my_phone = 'oz2nXjuKi6FO3iQz18AR7ArLIYAY'
        str_xml = web.data() #获得post来的数据
        try:
            xml = etree.fromstring(str_xml)#进行XML解析
            msgType = xml.find("MsgType").text
            lbg += '1'
            fromUser = xml.find("FromUserName").text
            lbg += '1'
            toUser = xml.find("ToUserName").text
            lbg += '1'
            content = self.process(xml.find("Content").text)  # 获得用户所输入的内容
            lbg += '2'
            return self.render.reply_text(fromUser,toUser,int(time.time()),u"..."+content)
        except Exception, e:
            try:
                lbg += '3'
                xml = etree.fromstring(str_xml)#进行XML解析
                lbg += '4'
                msgType = xml.find("MsgType").text
                lbg += '4'
                fromUser = xml.find("FromUserName").text
                lbg += '4'
                toUser = xml.find("ToUserName").text
                lbg += '4'
                if fromUser == my_phone:
                    except_str = u'_A_'
                    lbg += '5'
                    info = sys.exc_info()
                    lbg += '5'
                    for except_file, lineno, function, text in traceback.extract_tb(info[2]):
                        except_str = except_str + except_file + u' line: ' + str(
                            lineno) + u' in ' + function + u'\n' + u'\n'
                        # except_str = except_str + except_file+u' line: '+str(lineno)+u' in '+function+u'\n'+text+u'\n'
                    except_str += u"_B_** %s: %s" % info[:2]
                    lbg += '6'
                    return self.render.reply_text(fromUser,toUser,int(time.time()),lbg+u"__lbg__"+except_str)
                else:
                    return self.render.reply_text(fromUser,toUser,int(time.time()),lbg)
            except Exception, e:
                xml = etree.fromstring(str_xml)#进行XML解析
                lbg += '7'
                msgType = xml.find("MsgType").text
                fromUser = xml.find("FromUserName").text
                toUser = xml.find("ToUserName").text
                lbg += '8'
                if fromUser == my_phone:
                    lbg += '9'
                    return self.render.reply_text(fromUser,toUser,int(time.time()),lbg+u"_lbg_"+str(e))
                else:
                    return self.render.reply_text(fromUser,toUser,int(time.time()),lbg)

    def process(self, content):
        result = '???'
        if content == '233':
            file_name = os.listdir(os.path.dirname(__file__)+'/data_share')
            result = repr(file_name)
        elif content == '2331':
            # module_share.synHistory(['600229.SS'])
            result = str(module_share.test_requests())
        elif content == '2332':
            result = str(module_share.test_write())
        elif content == '2333':
            result = str(module_share_kelly.test_read())
        elif content == '2334':
            data = module_share.synHistory(['600229.SS'])
            result = str(float(module_share_kelly.load_share('600229.SS', data['600229.SS'])[1]))
        elif content.startswith('2335_'):
            try:
                share = content[5:]
                data = module_share.synHistory([share])
                result = str(float(module_share_kelly.load_share(share, data[share])[1]))
            except Exception, e:
                pass
        else:
            # result += str(random.random())
            pass
        return result

