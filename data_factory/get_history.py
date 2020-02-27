# -*- coding: utf-8 -*-
"""
-------------------------------------------------
   File Name：     get_history
   Description :
   Author :       yongyusu
   date：          2020/2/8
-------------------------------------------------
   Change Activity:
                   2020/2/8:
-------------------------------------------------
"""
import os
import baostock as bs
import pandas as pd
from stock_list import new_stock_list, stock_list


lg = bs.login()
print("login code and msg：", lg.error_code, lg.error_msg)

#http://baostock.com/baostock/index.php/A%E8%82%A1K%E7%BA%BF%E6%95%B0%E6%8D%AE
for stock in stock_list:
    file_name = "data/{}.csv".format(stock["name"])
    rs = bs.query_history_k_data(stock["code"],
                                "date, code ,open, high,low, close,preclose,\
                                volume,amount,turn,tradestatus,pctChg,isST,pbMRQ",
                                start_date='2017-01-01',
                                frequency="d", adjustflag="3")
    #print('query_history_k_data_plus respond error_code:'+rs.error_code)
    #print('query_history_k_data_plus respond  error_msg:'+rs.error_msg)

    #### 打印结果集 ####
    data_list = []
    while (rs.error_code == '0') & rs.next():
        # 获取一条记录，将记录合并在一起
        data_list.append(rs.get_row_data())
    result = pd.DataFrame(data_list, columns=rs.fields)

    #### 结果集输出到csv文件 ####
    if os.path.exists(file_name):
        os.remove(file_name)
    print("{} is done".format(file_name))
    result.to_csv(file_name, index=False)

#### 登出系统 ####
bs.logout()
