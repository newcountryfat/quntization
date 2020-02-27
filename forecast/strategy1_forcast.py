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


class StrategyVector:
    def __init__(self, name, code, increase_rate, day_after, pct_low_day_before):
        self.name = name
        self.code = code
        self.increase_rate = increase_rate
        self.day_after = day_after
        # 前一天降还是当天降：0是当天，1是前一天
        self.pct_low_day_before = pct_low_day_before


class StockDayInfo:
    def __init__(self, date, code, volume, pctChg):
        self.date = date
        self.code = code
        self.volume = volume
        self.pctChg = pctChg


def predict(day1: StockDayInfo, day2: StockDayInfo, day3: StockDayInfo, vector: StrategyVector) -> bool:
    """
    :param day1: 第一日信息
    :param day2: 第二日信息
    :param day3: 第三日信息
    :param vector: 对应策略
    :return: 返回N day后是否会涨（true 为涨）
    """
    statement3 = False
    if vector.pct_low_day_before == 0:
        if day3.pctChg < 0:
            statement3 = True
        else:
            return False
    if vector.pct_low_day_before == 1:
        if day2.pctChg < 0:
            statement3 = True
        else:
            return False
    statement1 = (day2.volume - day1.volume)/day1.volume > vector.increase_rate
    statement2 = (day3.volume - day2.volume)/day2.volume > vector.increase_rate
    return statement3 and statement1 and statement2


if __name__ == '__main__':
    #demo
    strategy_config_file = "forecast/strategy1_conf.csv"
    conf = pd.read_csv(strategy_config_file)
    for j in range(len(conf)):
        vector = StrategyVector(conf['name'][j], conf['code'][j], conf['increase_rate'][j],
                                conf['day_after'][j], conf['negative_day'][j])

        data_file_name = "data/{}.csv".format(vector.name)
        print("\n=========={}({}) now begin predict ==========".format(vector.name,vector.code))
        df = pd.read_csv(data_file_name)
        length = len(df)
        for i in range(length-4, length):
            day1 = StockDayInfo(df["date"][i-2], df["code"][i-2], df["volume"][i-2], df["pctChg"][i-2])
            day2 = StockDayInfo(df["date"][i-1], df["code"][i-1], df["volume"][i-1], df["pctChg"][i-1])
            day3 = StockDayInfo(df["date"][i], df["code"][i], df["volume"][i], df["pctChg"][i])
            if predict(day1, day2, day3, vector):
                print("{} days after {} will raise! winning rate is {}".format(vector.day_after,
                                                                               df["date"][i], conf['win_rate'][j]))
