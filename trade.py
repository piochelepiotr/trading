#! /usr/bin/python3
#import trading_api
import refresh_data
import pandas as pd
import websocket
import time
import json
import multiprocessing
import os
import numpy as np
import matplotlib.pyplot as plt
import candlestick
from matplotlib.finance import candlestick2_ohlc

folder = "data"
max_period = 3600*24*7//300
manager = multiprocessing.Manager()
data = {}
ns = manager.Namespace()
ns.c = 0
names = {7: 'BTC_BCN', 8: 'BTC_BELA', 10: 'BTC_BLK', 12: 'BTC_BTCD', 13: 'BTC_BTM', 14: 'BTC_BTS', 15: 'BTC_BURST', 20: 'BTC_CLAM', 24: 'BTC_DASH', 25: 'BTC_DGB', 27: 'BTC_DOGE', 28: 'BTC_EMC2', 31: 'BTC_FLDC', 32: 'BTC_FLO', 38: 'BTC_GAME', 40: 'BTC_GRC', 43: 'BTC_HUC', 50: 'BTC_LTC', 51: 'BTC_MAID', 58: 'BTC_OMNI', 60: 'BTC_NAUT', 61: 'BTC_NAV', 63: 'BTC_NEOS', 64: 'BTC_NMC', 66: 'BTC_NOTE', 69: 'BTC_NXT', 73: 'BTC_PINK', 74: 'BTC_POT', 75: 'BTC_PPC', 83: 'BTC_RIC', 86: 'BTC_SJCX', 89: 'BTC_STR', 92: 'BTC_SYS', 97: 'BTC_VIA', 98: 'BTC_XVC', 99: 'BTC_VRC', 100: 'BTC_VTC', 104: 'BTC_XBC', 108: 'BTC_XCP', 112: 'BTC_XEM', 114: 'BTC_XMR', 116: 'BTC_XPM', 117: 'BTC_XRP', 121: 'USDT_BTC', 122: 'USDT_DASH', 123: 'USDT_LTC', 124: 'USDT_NXT', 125: 'USDT_STR', 126: 'USDT_XMR', 127: 'USDT_XRP', 129: 'XMR_BCN', 130: 'XMR_BLK', 131: 'XMR_BTCD', 132: 'XMR_DASH', 137: 'XMR_LTC', 138: 'XMR_MAID', 140: 'XMR_NXT', 148: 'BTC_ETH', 149: 'USDT_ETH', 150: 'BTC_SC', 151: 'BTC_BCY', 153: 'BTC_EXP', 155: 'BTC_FCT', 158: 'BTC_RADS', 160: 'BTC_AMP', 162: 'BTC_DCR', 163: 'BTC_LSK', 166: 'ETH_LSK', 167: 'BTC_LBC', 168: 'BTC_STEEM', 169: 'ETH_STEEM', 170: 'BTC_SBD', 171: 'BTC_ETC', 172: 'ETH_ETC', 173: 'USDT_ETC', 174: 'BTC_REP', 175: 'USDT_REP', 176: 'ETH_REP', 177: 'BTC_ARDR', 178: 'BTC_ZEC', 179: 'ETH_ZEC', 180: 'USDT_ZEC', 181: 'XMR_ZEC', 182: 'BTC_STRAT', 183: 'BTC_NXC', 184: 'BTC_PASC', 185: 'BTC_GNT', 186: 'ETH_GNT', 187: 'BTC_GNO', 188: 'ETH_GNO'}

def load_data():
    files = os.listdir(folder)
    files = sorted(files)
    for filename in files:
        print("loading")
        currency = pd.read_csv(folder + os.sep + filename)
        name = filename[:len(filename)-4]
        currency_data = {}
        currency_data["close"] = manager.list(currency["close"].values[-max_period:])
        currency_data["open"] = manager.list(currency["open"].values[-max_period:])
        currency_data["low"] = manager.list(currency["low"].values[-max_period:])
        currency_data["high"] = manager.list(currency["high"].values[-max_period:])
        currency_data["date"] = manager.list(currency["date"].values[-max_period:])
        currency_data["change_1h"] = manager.list(candlestick.compute_change(currency["close"].values[-max_period:],10*3600//300))
        currency_data["buy_x"] = manager.list()
        currency_data["buy_y"] = manager.list()
        data[name] = currency_data

def init():
    #refresh_data.refresh_data()
    load_data()
    choose_buy_points()
    print("loaded")
    multiprocessing.Process(target=wamp_connect,args=()).start()
    print("launch commands")
    commands()
    #wamp_connect()

def on_message(ws, message):
    try:
        d = json.loads(message)
        ticker = d[2]
        t = int(time.time())
        ID = int(ticker[0])
        name = names[ID]
        if name[:3] == "BTC":
            name = name[4:]
            if name == "ETH":
                print("update ETH price : ",float(ticker[1]))
            else:
                print("other update")
            #data[name]["price"].append(float(ticker[1]))
            #data[name]["date"].append(t)
            ns.c += 1
    except:
        print("error on receiving ticker")

def on_error(ws, error):
    print(error)

def on_close(ws):
    print("### closed ###")

def on_open(ws):
    print("ONOPEN")
    def run(*args):
        #ws.send(json.dumps({'command':'subscribe','channel':1001}))
        ws.send(json.dumps({'command':'subscribe','channel':1002}))
        #ws.send(json.dumps({'command':'subscribe','channel':1003}))
        #ws.send(json.dumps({'command':'subscribe','channel':'BTC_XMR'}))
        while True:
            time.sleep(1)
        ws.close()
        print("thread terminating...")
    print("thread created")
    multiprocessing.Process(target=run,args=()).start()

def commands():
    while True:
        command = input("Enter a command\n")
        l = command.split()
        if len(l) == 0:
            print("Enter help for help")
        elif l[0] == "help":
            print("You can use :")
            print("exit -- to exit the program")
            print("holdings -- to have an overview of your different moneys")
            print("disp NAME -- displays NAME")
            print("moneys -- prints all the different moneys")
        elif l[0] == "holdings":
            print("not coded yet")
        elif l[0] == "exit":
            exit()
        elif l[0] == "disp":
            if len(l) == 2:
                name = l[1]
                if name in data:
                    fig,ax = plt.subplots(3,sharex=True)
                    candlestick2_ohlc(ax[0],data[name]['open'],data[name]['high'],data[name]['low'],data[name]['close'],width=0.6)
                    ax[0].plot(data[name]["buy_x"],data[name]["buy_y"],'go',color="red")
                    ax[0].set_title(name)
                    ax[1].plot(data[name]["change_1h"])
                    plt.show()
        elif l[0] == "moneys":
            print("different moneys :")
            for x in data:
                print(x)

def wamp_connect():
    print("connecting...")
    websocket.enableTrace(True)
    ws = websocket.WebSocketApp("wss://api2.poloniex.com/",
                              on_message = on_message,
                              on_error = on_error,
                              on_close = on_close)
    ws.on_open = on_open
    ws.run_forever()

if __name__ == "__main__":
    init()
