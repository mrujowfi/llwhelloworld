#coding=utf-8
__author__ = 'lw'
'''
http://summary.jrj.com.cn/hybk/index.shtml
概念板块ajax数据:http://q.jrjimg.cn/?q=cn|bk|5&n=hqa&c=l&o=pl,d&p=1050&_dc=1437575957282
行业板块ajax数据:http://q.jrjimg.cn/?q=cn|bk|7&n=hqa&c=l&o=pl,d&p=1050&_dc=1437576371462
地域板块ajax数据:http://q.jrjimg.cn/?q=cn|bk|3&n=hqa&c=l&o=pl,d&p=1050&_dc=1437576482336
证监会行业ajax数据:http://q.jrjimg.cn/?q=cn|bk|1&n=hqa&c=l&o=pl,d&p=1020&_dc=1437576515412
全球行业ajax数据:ttp://q.jrjimg.cn/?q=cn|bk|2&n=hqa&c=l&o=pl,d&p=1020&_dc=1437576648602
股票所属类别有交叉, 用逗号分开
某板块ajax数据:http://q.jrjimg.cn/?q=cn|s|bk400115932&c=m&n=hqa&o=pl,d&p=1050&_dc=1437740704114
'''
import requests
import time
import json
import os
import urllib
import datetime
import traceback
import module_share_kelly
import re
import pprint

global allShares, dictStart, getShares, dictPlate


# start_date & end_date 's format: yyyy-mm-dd
def get_historical_prices(symbol, start_date, end_date, proxies=None):
    params = urllib.urlencode({
        's': symbol,
        'a': int(start_date[5:7]) - 1,
        'b': int(start_date[8:10]),
        'c': int(start_date[0:4]),
        'd': int(end_date[5:7]) - 1,
        'e': int(end_date[8:10]),
        'f': int(end_date[0:4]),
        'g': 'd',
        'ignore': '.csv',
    })
    url = 'http://ichart.yahoo.com/table.csv?%s' % params
    # proxies = {
    #     "http": "http://123.58.129.48:443"
    # }
    req = requests.get(url, timeout=5, proxies=proxies)
    content = req.text
    daily_data = content.splitlines()
    hist_dict = dict()
    try:
        keys = daily_data[0].split(',')
        for day in daily_data[1:]:
            day_data = day.split(',')
            date = day_data[0]
            hist_dict[date] = \
                {keys[1]: day_data[1],
                 keys[2]: day_data[2],
                 keys[3]: day_data[3],
                 keys[4]: day_data[4],
                 keys[5]: day_data[5],
                 keys[6]: day_data[6]}
    except IndexError, e:
        print str(e)
        print content
        hist_dict = None
    return hist_dict

'''
先从股票列表里把所有股票查出来, 然后从2010到2015年都下下来保存, 记得要以股票名为文件名
如果失败就重来, 检测没有同名数据就从雅虎下载, 直到所有遍历
然后再遍历文件, 把每一天的均价扫进去, 计算涨跌, 保存到数据库, 再删除文件
出错则重新遍历文件, 直到没有文件.
'''


def synHistory(shares, date1='2015-01-01', date2='today'):
    result = {}
    listCode = list()
    for each in shares:
        listCode.append(each)
    print len(listCode)
    if date2 == 'today':
        startDate = date1
        endDate = datetime.datetime.now().strftime("%Y-%m-%d")
    else:
        startDate = date1
        endDate = date2
    # proxies = {"http": "http://112.74.86.238:3128"}
    proxies = None
    while True:
        try:
            for i in range(len(listCode)):
                each = listCode[i]
                print str(i)+'/'+str(len(listCode))
                # not in weixin
                # if os.path.exists(os.path.dirname(__file__)+'/data_share/'+each+'.txt'):
                #     os.remove(os.path.dirname(__file__)+'/data_share/'+each+'.txt')
                data = get_historical_prices(each, startDate, endDate, proxies)
                result[each] = data
                # not in weixin
                # f = open(os.path.dirname(__file__)+'/data_share/'+each+'.txt', 'w')
                # f.write(json.dumps(data, sort_keys=True, indent=4, separators=(',', ': ')))
                # f.close()
        except Exception, e:
            print 'step2 error:'+str(e)
            stack = traceback.format_exc()
            print stack
            if str(e).__contains__('10054') or str(e).__contains__('index out of'):
                print 'change proxies'
            time.sleep(5)
            continue
        break
    return result


def synShares(b_save_file=False):
    global allShares, dictStart, getShares, dictPlate
    try:
        f = open('step0.txt', 'r')
        f.close()
        os.remove('step0.txt')
    except Exception, e:
        pass
    try:
        f = open('share_name.txt', 'r')
        f.close()
        os.remove('share_name.txt')
    except Exception, e:
        pass
    while_count = 0
    while while_count<5:
        try:
            allShares = {}
            dictStart = {}
            dictStart['gainian']={}
            dictStart['hangye']={}
            dictStart['diyu']={}
            dictStart['zhengjianhui']={}
            dictStart['quanqiu']={}
            dictPlate = {}
            getShares = 'http://q.jrjimg.cn/?q=cn|s|{code}&c=m&n=hqa&o=pl,d&p={page}050&_dc='

            #概念
            req = getJrjimgUrl(u"http://q.jrjimg.cn/?q=cn|bk|5&n=hqa&c=l&o=pl,d&p=1050&_dc="+u'%d'%(time.time()*1000))
            dictStart['gainian']['pages'] = int( re.match(r'[\s\S]*?,pages:([0-9]*),', req.text[0:100]).group(1))
            dictStart['gainian']['name'] = u'概念'
            dictStart['gainian']['url'] = u"http://q.jrjimg.cn/?q=cn|bk|5&n=hqa&c=l&o=pl,d&p={page}050&_dc="
            # print 'gainian pages:'+str(dictStart['gainian']['pages'])

            #行业
            req = getJrjimgUrl(u"http://q.jrjimg.cn/?q=cn|bk|7&n=hqa&c=l&o=pl,d&p=1050&_dc="+u'%d'%(time.time()*1000))
            dictStart['hangye']['pages'] = int( re.match(r'[\s\S]*?,pages:([0-9]*),', req.text[0:100]).group(1))
            dictStart['hangye']['name'] = u'行业'
            dictStart['hangye']['url'] = u"http://q.jrjimg.cn/?q=cn|bk|7&n=hqa&c=l&o=pl,d&p=1050&_dc="
            # print 'hangye pages:'+str(dictStart['hangye']['pages'])

            #地域
            req = getJrjimgUrl(u"http://q.jrjimg.cn/?q=cn|bk|3&n=hqa&c=l&o=pl,d&p=1050&_dc="+u'%d'%(time.time()*1000))
            dictStart['diyu']['pages'] = int( re.match(r'[\s\S]*?,pages:([0-9]*),', req.text[0:100]).group(1))
            dictStart['diyu']['name'] = u'地域'
            dictStart['diyu']['url'] = u"http://q.jrjimg.cn/?q=cn|bk|3&n=hqa&c=l&o=pl,d&p={page}050&_dc="
            # print 'diyu pages:'+str(dictStart['diyu']['pages'])

            #证监会
            req = getJrjimgUrl(u"http://q.jrjimg.cn/?q=cn|bk|1&n=hqa&c=l&o=pl,d&p=1050&_dc="+u'%d'%(time.time()*1000))
            dictStart['zhengjianhui']['pages'] = int( re.match(r'[\s\S]*?,pages:([0-9]*),', req.text[0:100]).group(1))
            dictStart['zhengjianhui']['name'] = u'证监会'
            dictStart['zhengjianhui']['url'] = u"http://q.jrjimg.cn/?q=cn|bk|1&n=hqa&c=l&o=pl,d&p={page}050&_dc="
            # print 'zhengjianhui pages:'+str(dictStart['zhengjianhui']['pages'])

            #全球
            req = getJrjimgUrl(u"http://q.jrjimg.cn/?q=cn|bk|2&n=hqa&c=l&o=pl,d&p=1050&_dc="+u'%d'%(time.time()*1000))
            dictStart['quanqiu']['pages'] = int( re.match(r'[\s\S]*?,pages:([0-9]*),', req.text).group(1))
            dictStart['quanqiu']['name'] = u'全球'
            dictStart['quanqiu']['url'] = u"http://q.jrjimg.cn/?q=cn|bk|2&n=hqa&c=l&o=pl,d&p={page}050&_dc="
            # print 'quanqiu pages:'+str(dictStart['quanqiu']['pages'])

            #得到全部板块
            try:
                f = open('step0.txt', 'r')
                f.close()
            except IOError, e:
                # print 'exception1'+str(e)
                #本地无缓存全部板块
                for key in dictStart:
                    # print key
                    for i in range(1, int(dictStart[key]['pages'])+1):
                        req = getJrjimgUrl(dictStart[key]['url'].replace('{page}', str(i))+u'%d'%(time.time()*1000), timeout=10)
                        # print req.encoding#gbk
                        listPlate = eval(re.sub(r'^[\s\S]*?=({[\s\S]*});', r'\1', req.text).encode('utf-8'), type('Dummy', (dict,), dict(__getitem__=lambda s,n:n))())['HqData']
                        for each in listPlate:
                            # print each[0]
                            dictPlate[each[0]] = {}
                            dictPlate[each[0]]['code'] = each[0]
                            dictPlate[each[0]]['name'] = each[2]
                            # time.sleep(1)
                            req2 = getJrjimgUrl(u'http://q.jrjimg.cn/?q=cn|s|'+each[0]+'&c=m&n=hqa&o=pl,d&p=1050&_dc='+u'%d'%(time.time()*1000), timeout=10)
                            dictPlate[each[0]]['pages'] = int( re.match(r'[\s\S]*?,pages:([0-9]*),', req2.text).group(1))
                            dictPlate[each[0]]['url'] = getShares.replace('{code}', each[0])

                #缓存全部板块至本地
                f = open('step0.txt', 'w')
                f.write(json.dumps(dictPlate))
                f.close()

                # for key in dictPlate:
                #     print dictPlate[key]['code'], dictPlate[key]['name'], dictPlate[key]['pages'], dictPlate[key]['url']
                # print len(dictPlate)


            #得到所有股票
            conut = 0
            try:
                f = open('share_name.txt', 'r')
                f.close()
            except IOError, e:
                # print 'exception2'+str(e)
                #本地无缓存所有股票
                f = open('step0.txt', 'r')
                dictPlate = json.loads(f.read())
                f.close()
                for key in dictPlate:
                    # print key
                    for i in range(1, int(dictPlate[key]['pages'])+1):
                        # time.sleep(1)
                        req = getJrjimgUrl(dictPlate[key]['url'].replace('{page}', str(i))+u'%d'%(time.time()*1000), timeout=10)
                        #print req.encoding#gbk
                        listShares = eval(re.sub(r'^[\s\S]*?=({[\s\S]*});', r'\1', req.text).encode('utf-8'), type('Dummy', (dict,), dict(__getitem__=lambda s,n:n))())['HqData']
                        for each in listShares:
                            # print each[0]
                            if each[0].find('sh')>-1:
                                codeShare = each[1]+'.SS'
                            elif each[0].find('sz')>-1:
                                codeShare = each[1]+'.SZ'
                            else:
                                print 'error: unknown city'
                                continue
                            conut+=1
                            if allShares.has_key(codeShare):
                                pass
                                # allShares[codeShare]['plates'] = allShares[codeShare]['plates']+','+dictPlate[key]['name']
                            else:
                                allShares[codeShare] = {}
                                allShares[codeShare]['code'] = codeShare
                                allShares[codeShare]['name'] = each[2].replace(' ', '')
                                allShares[codeShare]['plates'] = '' # dictPlate[key]['name']

                # for key in allShares:
                #     print allShares[key]['code'], allShares[key]['name'], allShares[key]['plates']
                # print conut, len(allShares)

                #缓存所有股票至本地
                f = open('share_name.txt', 'w')
                f.write(json.dumps(allShares))
                f.close()

            if b_save_file==True:
                # print 'synShares finish(save file, no sql)'
                return

            # #保存至mysql
            # f = open('step1.txt', 'r')
            # allShares = json.loads(f.read())
            # f.close()
            # conn=MySQLdb.connect(host="192.168.50.128",port=3306,user="root",passwd="admin1234_abcd",db="db_shares",charset="utf8")
            # cursor = conn.cursor()
            # sql = "truncate table tb_shares"
            # cursor.execute(sql)
            # sql = "insert into tb_shares(code,name,plates) values(%s,%s,%s)"
            # for key in allShares:
            #     code = allShares[key]['code']
            #     name = allShares[key]['name']
            #     plates = allShares[key]['plates']
            #     print code, name, plates
            #     param = (code,name,plates)
            #     n = cursor.execute(sql,param)
            #     if n!=1:
            #         print 'error insert '+key
            #         continue
            # # sql = "insert into tb_shares(code,name,plates) values(%s,%s,%s)"
            # # code = '000001.SS'
            # # name = '上证指数'
            # # plates = '大盘'
            # # param = (code,name,plates)
            # # cursor.execute(sql,param)
            # cursor.close()
            # conn.commit()
            # conn.close()
            #
            # #os.remove('step0.txt')
            # #os.remove('step1.txt')
        except Exception, e:
            print 'exception3'+str(e)
            time.sleep(5)
            while_count += 1
            continue
        break
    return str(while_count)+' '

def getJrjimgUrl(url, timeout=30):
    while True:
        try:
            req = requests.get(url, timeout=timeout)
            if req.text.strip()=='':
                time.sleep(1)
                continue
        except Exception, e:
            time.sleep(5)
            continue
        break
    return req


def test_requests():
    resp = requests.get("http://llwhelloworld.applinzi.com/")
    return resp.content


def test_write():
    content = json.dumps({'test': 1}, sort_keys=True, indent=4, separators=(',', ': '))
    f = open(os.path.dirname(__file__)+'/data_share/test_file.txt', 'w')
    f.write(content)
    f.close()
    return content


if __name__ == '__main__':
    print os.path.dirname(__file__)
    data = synHistory(['600229.SS'])
    print module_share_kelly.load_share('600229.SS', data['600229.SS'])[1]
    print test_requests()
