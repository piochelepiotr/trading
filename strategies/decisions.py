#! /usr/bin/python3

import numpy as np

def manage_portfolio(moneys,period):
    n = len(moneys[list(moneys)[0]]['close'])
    m = len(moneys)
    buy_points_x = {}
    buy_points_y = {}
    sell_points_x = {}
    sell_points_y = {}
    moneys_amount = {}
    btc_equ_L = []
    b = []
    x = []
    eps = 1
    for name in moneys:
        buy_points_x[name] = []
        buy_points_y[name] = []
        sell_points_x[name] = []
        sell_points_y[name] = []
    for i in range(0,n,period):
        #balance portfolio
        total_btc = 1
        if i > 0:
            total_btc = sum([moneys_amount[name]*moneys[name]['close'][i] for name in moneys])
            x = [moneys[name]['close'][i]/moneys[name]['close'][i-period] for name in moneys]
            x_b = np.dot(x,[1/m]*m)
            diff = [xi - x_b for xi in x]
            to = max(0,(np.dot(b,x) - eps)/np.dot(diff,diff))
            b = [b[j] - to*diff[j] for j in range(m)]
        else:
            b = [1/m]*m
        print("bitcoin : ",total_btc)
        for j,name in enumerate(moneys):
            moneys_amount[name] = (b[j]*total_btc) / moneys[name]['close'][i]
        for j in range(i,min(i+period,n)):
            btc_equ_L.append(total_btc)
    for name in moneys:
        moneys[name]['btc_equ'] = btc_equ_L
    x_tot = [moneys[name]['close'][n-1]/moneys[name]['close'][0] for name in moneys]
    x_b_tot = np.dot(x_tot,[1/m]*m)
    print("var = ",x_b_tot)
    return buy_points_x,buy_points_y,sell_points_x,sell_points_y
