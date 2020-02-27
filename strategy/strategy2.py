# -*- coding: utf-8 -*-
"""
-------------------------------------------------
   File Name：     strategy2
   Description :   股票跌幅超过一定幅度且当日收盘价低于30日均线|15日均线|10日均线，回测第N天的胜率
   Author :       yongyusu
   date：          2020/2/9
-------------------------------------------------
   Change Activity:
                   2020/2/9:
-------------------------------------------------
"""

import pandas as pd
import numpy as np
from stock_list import stock_list, new_stock_list


avg_day_type = ["10days", "15days", "30days"]


def latest_avg_calculate(period, data_list):
    if len(data_list) < period:
        return sum(data_list)/len(data_list)
    else:
        return sum(data_list[-period:-1])/period


def avg_calculate(average_type, data_list):
    """
    计算日均数
    :param average_type:
    :param data_list:
    :return:
    """
    if average_type == "30days":
        return latest_avg_calculate(30, data_list)
    if average_type == "15days":
        return latest_avg_calculate(15, data_list)
    if average_type == "10days":
        return latest_avg_calculate(10, data_list)


def do_analyse(file, drop_scope, average_type, day_after):
    """
    :param file:
    :param drop_scope: 下跌幅度
    :param average_type: 日均线类型，30日，15日，10日
    :param day_after: N天
    """
    df = pd.read_csv(file)
    length = len(df)
    positive = 0
    total = 0
    for i in range(12, length - day_after):
        if df['pctChg'][i] < drop_scope and df['close'][i] < avg_calculate(average_type, df['close'][:i]):
            total += 1
            if df['pctChg'][i + day_after] > 0:
                positive += 1
    if total == 0:
        return 0
    win_rate = positive / total
    if total > 6 and win_rate > 0.8:
        print("drop_scope:{},average_type:{}, day_after:{}, win_rate_day:{}, "
              "total:{}".format(drop_scope, average_type, day_after, win_rate,  total))


if __name__ == '__main__':
    # 批量求胜率
    for stock in new_stock_list:
        file_name = "data/{}.csv".format(stock["name"])
        print("\n=========={}({},{}) now begin analyse ==========".format(stock['mark'], stock['name'],stock['code']))
        for pct in np.arange(-8.5, 0.5, 0.5):
            for day_type in avg_day_type:
                for day in range(1, 4):
                    do_analyse(file_name, pct, day_type, day)