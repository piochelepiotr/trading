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

def load_moneys(period,max_period,moneys):
    moneys = {}
    for name in moneys:
        print("loading ",name)
        moneys[name] = load_money(period,name)
    print("loaded")
    return moneys
