# coding=utf-8
__author__ = 'lw'

import json
import os

# f = (bp - cq) / (bc)

global share_data, except_data, money, cash, gu, sum_day, history, last_f
share_data = {}
except_data = {}
money = 100000.0
cash = 100000.0
gu = 0
sum_day = 0
history = 120
last_f = 0.0


def load_share(txt_name, data=None):
    global share_data, except_data, money, cash, gu, sum_day, history, last_f

    share_data = {}
    except_data = {}
    money = 10000.0
    cash = 10000.0
    gu = 0
    sum_day = 0
    history = 120
    if data is not None:
        share_data = data
    else:
        fin = open(os.path.dirname(__file__)+'/data_share/'+txt_name+'.txt')
        share_data = json.load(fin)
        fin.close()
    #print len(share_data)

    except_data = {}
    return count_f3(txt_name)

# ok
def count_f3(txt_name):
    global share_data, except_data, money, cash, gu, sum_day, history, last_f
    # b = max_last_week/last_close - 1
    # c = 1 - min_last_week/last_close

    if share_data is None:
        return
    keys = share_data.keys()
    keys.sort()
    keys = keys[-250:]
    #print len(keys)

    if len(keys) > 5:
        for i in range(history, len(keys)):
            max_last = 0
            min_last = 1000
            last_close = float(share_data[keys[i-1]]['Close'])
            up_percent = 0
            down_percent = 0
            for j in range(i-history, i):
                max_last = float(share_data[keys[j]]['Close']) if float(share_data[keys[j]]['Close']) > max_last else max_last
                min_last = float(share_data[keys[j]]['Close']) if float(share_data[keys[j]]['Close']) < min_last else min_last
            for j in range(i-5, i):
                if float(share_data[keys[j]]['Close']) >= float(share_data[keys[j]]['Open']):
                    up_percent += 1
                if float(share_data[keys[j]]['Close']) < float(share_data[keys[j]]['Open']):
                    down_percent += 1
            p = float(up_percent)/history
            q = float(down_percent)/history
            b = max_last/last_close - 1
            c = 1 - min_last/last_close
            # print keys[i],
            #print keys[i], b, c
            #print '\t', max_last_week, min_last_week, last_close
            if b*c != 0:
                f = (p*b - q*c)/(b*c)
            else:
                f = 0.5
            f = round(f, 2)
            # print f, max_last, min_last

            if f > 1:
                f = 1
            if f < 0:
                f = 0
            if last_close > max_last:
                f = 1
            if last_close < min_last:
                f = 0
            # print f

            trade(last_close, f)

    return summary(txt_name)

def trade(last_close, f):
    global share_data, except_data, money, cash, gu, sum_day, history, last_f

    money = cash + gu*last_close
    all_in = money*f
    if all_in > gu*last_close:
        # 买入
        gu_in = int((all_in - gu*last_close)/last_close)
        cash -= gu_in*last_close
        gu += gu_in
    elif all_in < gu*last_close:
        # 卖出
        gu_out = int((gu*last_close - all_in)/last_close)
        cash += gu_out*last_close
        gu -= gu_out
    money = cash + gu*last_close

    sum_day += 1
    last_f = f


def summary(txt_name):
    global share_data, except_data, money, cash, gu, sum_day, history, last_f

    print money
    return (str(money), str(last_f), str(sum_day))


def test_read():
    f = open(os.path.dirname(__file__)+'/data_share/test_file.txt')
    content = f.read()
    f.close()
    return content


if __name__ == '__main__':
    # file_name = os.listdir(r'G:\llw\code\python\shares\step')
    # result = {}
    # for i in range(len(file_name)):
    #     each = file_name[i]
    #     load_share(each)
    #     count_f3()
    #     print str(i)+'/'+str(len(file_name)),
    #     end = summary()
    #     result[each] = end
    # r_keys = result.keys()
    # r_keys.sort()
    # for each in r_keys:
    #     print ','.join(result[each])+','+each
    # print 'go'
    end = load_share('600229.SS')
    print end[1]



