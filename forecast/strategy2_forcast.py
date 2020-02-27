# -*- coding: utf-8 -*-
"""
-------------------------------------------------
   File Name：     strategy1_forecast
   Description :   基于strategy1, 对基金做预测
   Author :       yongyusu
   date：          2020/2/9
-------------------------------------------------
   Change Activity:
                   2020/2/9:
-------------------------------------------------
"""
import pandas as pd
from strategy.strategy2 import avg_calculate


class StrategyVector:
    def __init__(self, name, code, drop_scope, average_type, day_after):
        self.name = name
        self.code = code
        self.drop_scope = drop_scope
        self.day_after = day_after
        self.average_type = average_type


class StockDayInfo:
    def __init__(self, date, code, close, pctChg):
        self.date = date
        self.code = code
        self.close = close
        self.pctChg = pctChg


def predict(day: StockDayInfo, vector: StrategyVector, data_list) -> bool:
    """
    :param day: 当日信息
    :param vector: 对应策略
    :param data_list: 分析的数据list
    :return: 返回N day后是否会涨
    """
    statement1 = False
    if day.pctChg > vector.drop_scope:
        return False
    else:
        statement1 = True
    statement2 = day.close < avg_calculate(vector.average_type, data_list)
    return statement1 and statement2


if __name__ == '__main__':
    #demo
    strategy_config_file = "forecast/strategy2_conf.csv"
    conf = pd.read_csv(strategy_config_file)
    for j in range(len(conf)):
        vector = StrategyVector(conf['name'][j], conf['code'][j], conf['drop_scope'][j],
                                conf['average_type'][j], conf['day_after'][j])

        data_file_name = "data/{}.csv".format(vector.name)
        print("\n=========={}({}) now begin predict ==========".format(vector.name, vector.code))
        df = pd.read_csv(data_file_name)
        length = len(df)
        for i in range(length-6, length):
            day1 = StockDayInfo(df["date"][i], df["code"][i], df["close"][i], df["pctChg"][i])
            if predict(day1, vector, df["close"][i-50:i]):
                print("{} days after {} will raise! winning rate is {}".format(vector.day_after,
                                                                               df["date"][i], conf['win_rate'][j]))
