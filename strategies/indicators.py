#! /usr/bin/python3

import math
import numpy as np

def bollinger_bands(open_prices,period = 20,delta = 2):
    n = len(open_prices)
    p = open_prices[0]
    middle_line = [p]*(period-1)
    up_line = [p]*(period-1)
    down_line = [p]*(period-1)
    for i in range(period-1,n):
        average = sum(open_prices[i-period+1:i+1]) / period
        stand_dev = 0
        for p in open_prices[i-period+1:i+1]:
            stand_dev += pow(p-average,2)
        stand_dev = math.sqrt(stand_dev/period)
        middle_line.append(average)
        up_line.append(average+delta*stand_dev)
        down_line.append(average-delta*stand_dev)
    return down_line,middle_line,up_line

def ema(close_prices,period):
    #(1-lamb)^n = 0.5
    lamb = 1-pow(0.5,1/period)
    ema=close_prices[0]
    emas=[]
    for p in close_prices:
        ema = (1-lamb)*ema + lamb*p
        emas.append(ema)
    return emas

def average(close_prices,period):
    av = []
    L = [close_prices[0]]*period
    s = sum(L)
    for i in close_prices:
        s -= L[0]
        L = L[1:]
        L.append(i)
        s += i
        av.append(s/period)
    return av

def compute_diff(L1,L2):
    return [L1[i] - L2[i] for i in range(len(L1))]

def macd(close_prices,short_period=12,long_period=26,macd_period=9):
    short_ema = ema(close_prices,short_period)
    long_ema = ema(close_prices,long_period)
    macd = compute_diff(short_ema,long_ema)
    signal_line = ema(macd,macd_period)
    return macd,signal_line

def change(close_prices,period):
    return [(close_prices[i]/close_prices[max(0,i-period)] - 1)*100 for i in range(len(close_prices))]

def absolute_change(prices,period):
    return [prices[i] - prices[max(0,i-period)] for i in range(len(prices))]

def rsi(close_prices,period):
    rsi_L = []
    n = len(close_prices)
    change = absolute_change(close_prices,1)
    up = [max(0,c) for c in change]
    down = [abs(min(0,c)) for c in change]
    U = ema(up,period)
    D = ema(down,period)
    for i in range(n):
        if U[i] == 0 and D[i] == 0:
            rsi_L.append(50)
        else:
            rsi_L.append(U[i]/(U[i]+D[i])*100)
    return rsi_L

def percent_line(close_prices,percent,period):
    n = len(close_prices)
    line = []
    for i in range(n):
        tab = close_prices[max(0,i-period+1):i+1]
        ind = min(len(tab)-1,int(len(tab)*(percent/100)))
        line.append(np.sort(tab)[ind])
    return line

def price_min(close_prices,period):
    return [min(close_prices[max(0,i-period):i+1]) for i in range(len(close_prices))]

def price_max(close_prices,period):
    return [max(close_prices[max(0,i-period):i+1]) for i in range(len(close_prices))]



