#! /usr/bin/python3

from matplotlib.finance import candlestick2_ohlc
import matplotlib.pyplot as plt
import load_data
import pamr
import params
import ressemblance


def plot(data,name):
    n = len(data['close'])
    fig,ax = plt.subplots(3,sharex=True)
    candlestick2_ohlc(ax[0],data['open'],data['high'],data['low'],data['close'],width=0.6)
    ax[1].plot(data['btc_equ'])
    ax[2].plot(data['average_gains'])
    ax[0].set_title(name)
    plt.show()

period = 300
max_period = 3600*24
moneys = load_data.load_moneys(period,max_period,params.moneys)
#ressemblance.ressemblances(moneys,(12*300)//period)

for i in range(6,15):
#i = 2
    print("for i = ",i)
    pamr.manage_portfolio_past(moneys,(i*300)//period)
for name in moneys:
    #name = list(moneys)[0]
    plot(moneys[name],name)

