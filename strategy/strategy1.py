# -*- coding: utf-8 -*-
"""
-------------------------------------------------
   File Name：     strategy1
   Description :   demo:连续2天成交量放量的情况(第二天下跌），回测第N日的收益正负
   Author :       yongyusu
   date：          2020/2/8
-------------------------------------------------
   Change Activity:
                   2020/2/8:
-------------------------------------------------
"""

import pandas as pd
import numpy as np
from stock_list import stock_list, new_stock_list


def calculate_volume_increase(a, b, rate):
    if a == 0 or b == 0:
        return False
    else:
        return (float(b)-float(a))/a > rate


def do_analyse(file, volume_increase, day_after):
    df = pd.read_csv(file)
    length = len(df)
    positive = 0
    positive1 = 0
    total = 0
    total1 = 0

    #print(df['date'][0])
    for i in range(2, length - day_after):
        b1 = calculate_volume_increase(df['volume'][i-2], df['volume'][i-1], volume_increase)
        b2 = calculate_volume_increase(df['volume'][i-1], df['volume'][i], volume_increase)
        if b1 and b2 and df['pctChg'][i] < 0:
            total += 1
            if df['pctChg'][i+day_after] > 0:
                positive += 1
        if b1 and b2 and df['pctChg'][i-1] < 0:
            total1 += 1
            if df['pctChg'][i+day_after] > 0:
                positive1 += 1
    #print("match strategy {} times , positive :{}, negtive :{},"
    #      "winning probability:{} ".format(total, positive, negtive, positive/total))
    if total1==0 or total == 0:
        return 0
    win_rate = positive/total
    win_rate_new = positive1/total1
    if (win_rate > 0.8 and total > 6) or (win_rate_new > 0.8 and total1 > 6):
        print("increase_rate:{}, day_after:{},"
              " win_rate_day:{},win_rate_day_before:{}, "
              "total:{}, total_day_before:{}".format(volume_increase, day_after, win_rate, win_rate_new, total, total1))


if __name__ == '__main__':
    # 批量求胜率
    for stock in stock_list:
        file_name = "data/{}.csv".format(stock["name"])
        print("\n=========={}({}:{}) now begin analyse ==========".format(stock['mark'], stock['name'], stock['code']))
        for v in np.arange(0.04, 0.26, 0.02):
            for day in range(1, 6):
                do_analyse(file_name, v, day)






