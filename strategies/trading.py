#! /usr/bin/python3

from matplotlib.finance import candlestick2_ohlc
import matplotlib.pyplot as plt
import indicators
import load_data
import decisions

def plot(data,name,buy_points_x,buy_points_y,sell_points_x,sell_points_y):
    n = len(data['close'])
    fig,ax = plt.subplots(3,sharex=True)
    candlestick2_ohlc(ax[0],data['open'],data['high'],data['low'],data['close'],width=0.6)
    ax[0].plot(buy_points_x,buy_points_y,'go',color='#00ff00')
    ax[0].plot(sell_points_x,sell_points_y,'go',color='red')
    #ax[0].plot(data['min_week'])
    #ax[0].plot(data['max_week'])
    #ax[0].plot(data['min_month'])
    #ax[0].plot(data['bollinger_middle'],color='grey')
    #ax[0].plot(data['bollinger_down'],color='blue')
    #ax[0].plot(data['bollinger_up'],color='blue')
    #ax[1].plot(data['macd'])
    #ax[1].plot(data['signal_line'])
    #ax[1].plot([0]*n)
    #ax[1].plot(data["long_term"])
    #ax[1].plot(data["short_term"])
    #ax[1].plot(data["change_24h"])
    #ax[1].plot([0]*n)
    ax[2].plot(data['btc_equ'])
    #ax[2].plot([30]*n)
    #ax[2].plot([60]*n)
    #ax[2].plot(data['rsi'])
    ax[0].set_title(name)
    plt.show()

def test_trade(period,name):
    data = load_data.load_money(period,name)
    plot(data,name)

#for name in load_data.currency_list:
#    test_trade(900,name)

period = 300
moneys = load_data.load_moneys(period)
#buy_points_x,buy_points_y,sell_points_x,sell_points_y = decisions.manage_portfolio(moneys,(3600)//period)
#for name in moneys:
#    #if len(buy_points_x[name]) > 0:
#    plot(moneys[name],name,buy_points_x[name],buy_points_y[name],sell_points_x[name],sell_points_y[name])

