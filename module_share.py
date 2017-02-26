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
