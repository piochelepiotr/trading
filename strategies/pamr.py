#! /usr/bin/python3

import numpy as np

def compute_portfolio(prev_b,x):
    eps = 1
    m = len(prev_b)
    x_b = np.dot(x,[1/m]*m)
    diff = [xi - x_b for xi in x]
    norm = np.dot(diff,diff)
    to = 0
    if norm != 0:
        to = max(0,(np.dot(prev_b,x) - eps)/np.dot(diff,diff))
    b = [prev_b[j] - to*diff[j] for j in range(m)]
    return b

def manage_portfolio(moneys,period):
    n = len(moneys[list(moneys)[0]]['close'])
    m = len(moneys)
    moneys_amount = {}
    btc_equ_L = []
    b = []
    old_moneys = []
    for i in range(0,n,period):
        #balance portfolio
        total_btc = 1
        if i > 0:
            total_btc = sum([moneys_amount[name]*moneys[name]['close'][i] for name in moneys])
            x = [moneys[name]['close'][i]/moneys[name]['close'][i-period] for name in moneys]
            prev_b = b
            b = compute_portfolio(b,x)
            total_move = sum([abs(prev_b[j] - b[j]) for j in range(m)])
            total_btc -= total_btc*total_move*0.004
        else:
            b = [1/m]*m
            old_moneys = [0]*m
        #print("bitcoin : ",total_btc)
        for j,name in enumerate(moneys):
            moneys_amount[name] = (b[j]*total_btc) / moneys[name]['close'][i]
        for j in range(i,min(i+period,n)):
            btc_equ_L.append(total_btc)
    for name in moneys:
        moneys[name]['btc_equ'] = btc_equ_L
    x_tot = [moneys[name]['close'][n-1]/moneys[name]['close'][0] for name in moneys]
    x_b_tot = np.dot(x_tot,[1/m]*m)
    print("end btc : ",btc_equ_L[-1])
    print("var = ",x_b_tot)
