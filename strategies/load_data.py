#! /usr/bin/python3

import pandas as pd
import indicators
import os
import compute_stats

max_period = 3600*24*30*6
data_folder_base = "data_"

currency_list = ['AMP','ARDR','BCN','BCY','BELA','BLK','BTCD','BTM','BTS','BURST','CLAM','DASH','DCR','DGB','DOGE','EMC2','ETC','ETH','EXP','FCT','FLDC','FLO','GAME','GNO','GNT','GRC','HUC','LBC','LSK','LTC','MAID','NAUT','NAV','NEOS','NMC','NOTE','NXC','NXT','OMNI','PASC','PINK','POT','PPC','RADS','REP','RIC','SBD','SC','SJCX','STEEM','STR','STRAT','SYS','VIA','VRC','VTC','XBC','XCP','XEM','XMR','XPM','XRP','XVC','ZEC']

def load_money(period,name):
    number_points = max_period // period
    data_folder = data_folder_base + str(period)
    data = pd.read_csv(data_folder + os.sep + name + '.csv')
    index_to_keep = list(range(len(data)-number_points,len(data)))
    data = data.take(index_to_keep)
    data = data.reset_index()
    return data

def load_moneys(period):
    moneys = {}
    for name in currency_list[:15]:#["ETH","XMR","LTC","XRP","DGB"]:#currency_list
        print("loading ",name)
        moneys[name] = load_money(period,name)
    print("loaded")
    return moneys
