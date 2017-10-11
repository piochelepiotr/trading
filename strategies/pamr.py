#! /usr/bin/python3

import numpy as np

fee = 0.003#(so 0.25%)

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

def compute_amounts(prev_b,b,holdings,price,moneys):
    m = len(moneys)
    amounts = [holdings[name]*price[j] for j,name in enumerate(moneys)]
    total_btc = sum(amounts)
    total_move = sum([abs(prev_b[j] - b[j]) for j in range(m)])
    total_btc_after = total_btc - total_btc*total_move*fee
    amounts_after = [total_btc_after*b[j] for j in range(m)]
    amounts_diff = [amounts_after[j] - amounts[j] for j in range(m)]
    return amounts_diff,total_btc

def sell_moneys(amounts,bids,moneys,holdings):
    #amounts are in coins
    btc = 0
    #ask > bid so ask = sell price, bid = buy price
    for i,x in enumerate(amounts):
        if x < 0:
            x = min(holdings[moneys[i]],abs(x))
            #sell
            btc += x*bids[moneys[i]]*(1-fee)
            holdings[moneys[i]] -= x
    return btc

def buy_moneys(amounts,asks,moneys,btc,holdings):
    #amounts are in btc
    total_buy = sum([0 if a < 0 else a for a in amounts])
    for i,a in enumerate(amounts):
        if a > 0:
            holdings[moneys[i]] += (((a/total_buy)*btc) / asks[moneys[i]])*(1-fee)

def manage_portfolio_past(moneys,period):
    n = len(moneys[list(moneys)[0]]['close'])
    m = len(moneys)
    holdings = {}
    btc_equ_L = []
    average_gains = []
    b = []
    last_i = 0
    for i in range(0,n,period):
        last_i = i
        #balance portfolio
        total_btc = 1
        gain = 1
        price = [moneys[name]['close'][i] for name in moneys]
        if i > 0:
            gain = sum([moneys[name]['close'][i]/moneys[name]['close'][0] for name in moneys])/m
            asks = {}
            bids = {}
            for j,name in enumerate(moneys):
                asks[name] = price[j]
                bids[name] = price[j]
            x = [price[j]/moneys[name]['close'][i-period] for j,name in enumerate(moneys)]
            prev_b = b
            b = compute_portfolio(b,x)
            amounts,total_btc = compute_amounts(prev_b,b,holdings,price,list(moneys))
            btc = sell_moneys([a/price[j] for j,a in enumerate(amounts)],bids,list(moneys),holdings)
            buy_moneys(amounts,asks,list(moneys),btc,holdings)
        else:
            b = [1/m]*m
            for j,name in enumerate(moneys):
                holdings[name] = (total_btc/m)/price[j]
        #print("bitcoin : ",total_btc)
        for j in range(i,min(i+period,n)):
            btc_equ_L.append(total_btc)
            average_gains.append(gain)
    for name in moneys:
        moneys[name]['btc_equ'] = btc_equ_L
        moneys[name]['average_gains'] = average_gains
    x_tot = [moneys[name]['close'][n-1]/moneys[name]['close'][0] for name in moneys]
    print("end btc : ",btc_equ_L[-1])
    print("var = ",sum(x_tot)/m)
    return [moneys[name]['close'][last_i] for name in list(moneys)],b,moneys[list(moneys)[0]]['date'][last_i]
