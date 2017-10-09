#! /usr/bin/python3

from matplotlib.finance import candlestick2_ohlc
import matplotlib.pyplot as plt
import load_data
import pamr

def plot(data,name):
    n = len(data['close'])
    fig,ax = plt.subplots(3,sharex=True)
    candlestick2_ohlc(ax[0],data['open'],data['high'],data['low'],data['close'],width=0.6)
    ax[1].plot(data['btc_equ'])
    ax[0].set_title(name)
    plt.show()

period = 300
moneys = load_data.load_moneys(period)
#for i in range(1,10):
pamr.manage_portfolio(moneys,(1*600)//period)
#for name in moneys:
#    plot(moneys[name],name)

