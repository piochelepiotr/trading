#! /usr/bin/python3

import indicators
import pandas as pd
import os
import compute_stats

max_period = 3600*24*7*1
data_folder_base = "data_"

currency_list = ['AMP','ARDR','BCN','BCY','BELA','BLK','BTCD','BTM','BTS','BURST','CLAM','DASH','DCR','DGB','DOGE','EMC2','ETC','ETH','EXP','FCT','FLDC','FLO','GAME','GNO','GNT','GRC','HUC','LBC','LSK','LTC','MAID','NAUT','NAV','NEOS','NMC','NOTE','NXC','NXT','OMNI','PASC','PINK','POT','PPC','RADS','REP','RIC','SBD','SC','SJCX','STEEM','STR','STRAT','SYS','VIA','VRC','VTC','XBC','XCP','XEM','XMR','XPM','XRP','XVC','ZEC']

def load_money(period,name):
    number_points = max_period // period
    data_folder = data_folder_base + str(period)
    data = pd.read_csv(data_folder + os.sep + name + '.csv')
    index_to_keep = list(range(len(data)-number_points,len(data)))
    data = data.take(index_to_keep)
    data = data.reset_index()
    data['rsi'] = indicators.rsi(data['close'],14)
    data['change_24h'] = indicators.change(data['close'],(3600*24)//period)
    macd,signal_line = indicators.macd(data['close'])
    data['macd'] = macd
    data['signal_line'] = signal_line
    compute_stats.compute_move(data,3,3)
    compute_stats.stat_up(data)
    for i in range(9):
        compute_stats.stat_up_rsi(data,10*i,10*(i+1))
    for i in range(-3,3):
        compute_stats.stat_up_change24h(data,10*i,10*(i+1))
    #add indicators
    #down_line,middle_line,up_line = indicators.bollinger_bands(data['open'])
    #data['bollinger_up'] = up_line
    #data['bollinger_down'] = down_line
    #data['bollinger_middle'] = middle_line
    #data['change_24h'] = indicators.change(data['close'],(3600)//period)
    #data['min_week'] =  indicators.price_min(data['close'],(3600*24*7)//period)
    #data['min_month'] = indicators.price_min(data['close'],(3600*24*30)//period)
    #data['max_week'] =  indicators.price_max(data['close'],(3600*24*7)//period)
    #data["long_term"] = indicators.ema(data["close"],30)
    #data['percent_line'] = indicators.percent_line(data['close'],10,(3600*24*2)//period)
    #data['percent_line_2'] = indicators.percent_line(data['close'],10,(3600*2)//period)
    return data

def load_moneys(period):
    moneys = {}
    for name in ["ETH","XMR","LTC","XRP","DGB"]:#currency_list
        print("loading ",name)
        moneys[name] = load_money(period,name)
    print("loaded")
    return moneys
