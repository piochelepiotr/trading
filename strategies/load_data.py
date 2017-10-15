#! /usr/bin/python3

import pandas as pd
import os

data_folder_base = "data_"


def load_money(period,name,max_period):
    number_points = max_period // period
    data_folder = data_folder_base + str(period)
    data = pd.read_csv(data_folder + os.sep + name + '.csv')
    index_to_keep = list(range(len(data)-number_points,len(data)))
    data = data.take(index_to_keep)
    data = data.reset_index()
    return data

def adapt_moneys(moneys,period):
    names = list(moneys)
    first = moneys[names[0]]
    n = len(first['date'])
    min_date = first['date'][n-1]
    max_date = 0
    for name in names:
        if moneys[name]['date'][n-1] < min_date:
            min_date = moneys[name]['date'][n-1]
        if moneys[name]['date'][n-1] > max_date:
            max_date = moneys[name]['date'][n-1]
    diff = (max_date - min_date) // period
    for name in names:
        last = moneys[name]['date'][n-1]
        #remove from the end
        end = (last - min_date)//period
        #remove the rest from the beginning
        begin = diff - end
        index_to_keep = list(range(begin,n-end))
        moneys[name] = moneys[name].take(index_to_keep).reset_index()
    return moneys

def load_moneys(period,max_period,moneys_names):
    moneys = {}
    for name in moneys_names:
        print("loading ",name)
        moneys[name] = load_money(period,name,max_period)
        print(moneys[name]['date'][len(moneys[name]['date'])-1])
    moneys = adapt_moneys(moneys,period)
    #for name in moneys_names:
    #    print("checking ",name)
    #    print("len = ",len(moneys[name]['date']))
    #    print(moneys[name]['date'][len(moneys[name]['date'])-1])
    print("loaded")
    return moneys
