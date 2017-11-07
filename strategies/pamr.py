#! /usr/bin/python3

import numpy as np

fee = 0.00#(so 0.25%)

def compute_portfolio(prev_b,x):
    eps = 1
    m = len(prev_b)
    moneys = list(prev_b)
    x_L = [x[name] for name in moneys]
    prev_b_L = [prev_b[name] for name in moneys]
    x_b = np.dot(x_L,[1/m]*m)
    diff = [xi - x_b for xi in x_L]
    norm = np.dot(diff,diff)
    to = 0
    if norm != 0:
        to = max(0,(np.dot(prev_b_L,x_L) - eps)/np.dot(diff,diff))
    b = {name : prev_b_L[j] - to*diff[j] for j,name in enumerate(moneys)}
    return b

def compute_amounts(prev_b,b,holdings,price):
    amounts = {name : holdings[name]*price[name] for name in holdings}
    total_btc = sum(list(amounts.values()))
    total_move = sum([abs(prev_b[name] - b[name]) for name in b])
    total_btc_after = total_btc - total_btc*total_move*fee
    amounts_after = {name : total_btc_after*b[name] for name in b}
    amounts_diff = {name :amounts_after[name] - amounts[name] for name in b}
    return amounts_diff,total_btc

def sell_moneys(amounts,bids,holdings):
    #amounts are in coins
    btc = 0
    #ask > bid so ask = sell price, bid = buy price
    for name in amounts:
        if amounts[name] < 0:
            x = min(holdings[name],abs(amounts[name]))
            #sell
            btc += x*bids[name]*(1-fee)
            holdings[name] -= x
    return btc

def buy_moneys(amounts,asks,btc,holdings):
    #amounts are in btc
    total_buy = sum([0 if amounts[name] < 0 else amounts[name] for name in amounts])
    for name in amounts:
        if amounts[name] > 0:
            holdings[name] += (((amounts[name]/total_buy)*btc) / asks[name])*(1-fee)

def manage_portfolio_past(moneys,period):
    n = len(moneys[list(moneys)[0]]['close'])
    m = len(moneys)
    holdings = {}
    btc_equ_L = []
    average_gains = []
    b = {}
    last_i = 0
    for i in range(0,n,period):
        last_i = i
        #balance portfolio
        total_btc = 1
        gain = 1
        price = {name : moneys[name]['close'][i] for name in moneys}
        if i > 0:
            gain = sum([moneys[name]['close'][i]/moneys[name]['close'][0] for name in moneys])/m
            asks = {}
            bids = {}
            for name in moneys:
                asks[name] = price[name]
                bids[name] = price[name]
            x = {name : price[name]/moneys[name]['close'][i-period] for name in moneys}
            prev_b = b
            b = compute_portfolio(b,x)
            amounts,total_btc = compute_amounts(prev_b,b,holdings,price)
            btc = sell_moneys({name:amounts[name]/price[name] for name in amounts},bids,holdings)
            buy_moneys(amounts,asks,btc,holdings)
        else:
            b = {name : 1/m for name in moneys}
            holdings = {name : (total_btc/m)/price[name] for name in moneys}
        #print("bitcoin : ",total_btc)
        for j in range(i,min(i+period,n)):
            btc_equ_L.append(total_btc)
            average_gains.append(gain)
    for name in moneys:
        moneys[name]['btc_equ'] = btc_equ_L
        moneys[name]['average_gains'] = average_gains
    x_tot = [moneys[name]['close'][last_i]/moneys[name]['close'][0] for name in moneys]
    print("end btc : ",btc_equ_L[-1])
    print("var = ",sum(x_tot)/m)
    return {name : moneys[name]['close'][last_i] for name in list(moneys)},b,moneys[list(moneys)[0]]['date'][last_i]
