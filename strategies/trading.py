#! /usr/bin/python3

from matplotlib.finance import candlestick2_ohlc
import matplotlib.pyplot as plt
import indicators
import load_data
import decisions
import compute_stats

def plot(data,name,buy_points_x,buy_points_y,sell_points_x,sell_points_y):
    n = len(data['close'])
    fig,ax = plt.subplots(3,sharex=True)
    candlestick2_ohlc(ax[0],data['open'],data['high'],data['low'],data['close'],width=0.6)
    ax[0].plot(buy_points_x,buy_points_y,'go',color='#00ff00')
    ax[0].plot(sell_points_x,sell_points_y,'go',color='red')
    ax[1].plot(data['btc_equ'])
    ax[0].set_title(name)
    plt.show()

def test_trade(period,name):
    data = load_data.load_money(period,name)
    plot(data,name)

#for name in load_data.currency_list:
#    test_trade(900,name)

period = 300
moneys = load_data.load_moneys(period)
buy_points_x,buy_points_y,sell_points_x,sell_points_y = decisions.manage_portfolio(moneys,(2*3600)//period)
for name in moneys:
    #buy_points_x,buy_points_y,sell_points_x,sell_points_y = compute_stats.market_maker(moneys[name])#compute_stats.stat_up_macd(moneys[name])
    plot(moneys[name],name,buy_points_x[name],buy_points_y[name],sell_points_x[name],sell_points_y[name])

