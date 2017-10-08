#! /usr/bin/python3

from matplotlib.finance import candlestick2_ohlc
import matplotlib.pyplot as plt
import load_data
import decisions

def plot(data,name):
    n = len(data['close'])
    fig,ax = plt.subplots(3,sharex=True)
    candlestick2_ohlc(ax[0],data['open'],data['high'],data['low'],data['close'],width=0.6)
    ax[1].plot(data['btc_equ'])
    ax[0].set_title(name)
    plt.show()

period = 300
moneys = load_data.load_moneys(period)
buy_points_x,buy_points_y,sell_points_x,sell_points_y = decisions.manage_portfolio(moneys,(2*3600)//period)
for name in moneys:
    plot(moneys[name],name)

