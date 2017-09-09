#! /usr/bin/python3
import pandas as pd
import time
import multiprocessing
import os
import numpy as np
import websocket
import trading_api

manager = multiprocessing.Manager()
ns = manager.Namespace()
current_prices = manager.dict()
ns.c = 0
names = {7: 'BTC_BCN', 8: 'BTC_BELA', 10: 'BTC_BLK', 12: 'BTC_BTCD', 13: 'BTC_BTM', 14: 'BTC_BTS', 15: 'BTC_BURST', 20: 'BTC_CLAM', 24: 'BTC_DASH', 25: 'BTC_DGB', 27: 'BTC_DOGE', 28: 'BTC_EMC2', 31: 'BTC_FLDC', 32: 'BTC_FLO', 38: 'BTC_GAME', 40: 'BTC_GRC', 43: 'BTC_HUC', 50: 'BTC_LTC', 51: 'BTC_MAID', 58: 'BTC_OMNI', 60: 'BTC_NAUT', 61: 'BTC_NAV', 63: 'BTC_NEOS', 64: 'BTC_NMC', 66: 'BTC_NOTE', 69: 'BTC_NXT', 73: 'BTC_PINK', 74: 'BTC_POT', 75: 'BTC_PPC', 83: 'BTC_RIC', 86: 'BTC_SJCX', 89: 'BTC_STR', 92: 'BTC_SYS', 97: 'BTC_VIA', 98: 'BTC_XVC', 99: 'BTC_VRC', 100: 'BTC_VTC', 104: 'BTC_XBC', 108: 'BTC_XCP', 112: 'BTC_XEM', 114: 'BTC_XMR', 116: 'BTC_XPM', 117: 'BTC_XRP', 121: 'USDT_BTC', 122: 'USDT_DASH', 123: 'USDT_LTC', 124: 'USDT_NXT', 125: 'USDT_STR', 126: 'USDT_XMR', 127: 'USDT_XRP', 129: 'XMR_BCN', 130: 'XMR_BLK', 131: 'XMR_BTCD', 132: 'XMR_DASH', 137: 'XMR_LTC', 138: 'XMR_MAID', 140: 'XMR_NXT', 148: 'BTC_ETH', 149: 'USDT_ETH', 150: 'BTC_SC', 151: 'BTC_BCY', 153: 'BTC_EXP', 155: 'BTC_FCT', 158: 'BTC_RADS', 160: 'BTC_AMP', 162: 'BTC_DCR', 163: 'BTC_LSK', 166: 'ETH_LSK', 167: 'BTC_LBC', 168: 'BTC_STEEM', 169: 'ETH_STEEM', 170: 'BTC_SBD', 171: 'BTC_ETC', 172: 'ETH_ETC', 173: 'USDT_ETC', 174: 'BTC_REP', 175: 'USDT_REP', 176: 'ETH_REP', 177: 'BTC_ARDR', 178: 'BTC_ZEC', 179: 'ETH_ZEC', 180: 'USDT_ZEC', 181: 'XMR_ZEC', 182: 'BTC_STRAT', 183: 'BTC_NXC', 184: 'BTC_PASC', 185: 'BTC_GNT', 186: 'ETH_GNT', 187: 'BTC_GNO', 188: 'ETH_GNO'}

def load_data():
    files = os.listdir(folder)
    files = sorted(files)
    for filename in files:
        name = filename[:len(filename)-4]
        print("loading",name)
        current_prices[name] = 0

def init():
    #refresh_data.refresh_data()
    load_data()
    choose_buy_points()
    print("loaded")
    multiprocessing.Process(target=wamp_connect,args=()).start()
    print("launch commands")
    commands()

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
            current_prices[name] = float(ticker[1])
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

def wamp_connect():
    print("connecting...")
    websocket.enableTrace(True)
    ws = websocket.WebSocketApp("wss://api2.poloniex.com/",
                              on_message = on_message,
                              on_error = on_error,
                              on_close = on_close)
    ws.on_open = on_open
    ws.run_forever()

def load_config():
    print("load config")
    config = {}
    data = pd.read_csv("config.csv")
    for i,name in enumerate(data["name"]):
        config[name] = {}
        config[name]["buy_price"] = data["buy_price"][i]
        config[name]["sell_price"] = data["sell_price"][i]
        config[name]["stop_loss_price"] = data["stop_loss_price"][i]
        config[name]["signal_buy_price"] = data["signal_buy_price"][i]
        if config[name]["buy_price"] <= 0:
            print("buy price at 0")
            exit()
        if config[name]["signal_buy_price"] <= 0:
            print("signal buy price at 0")
            exit()
        if config[name]["sell_price"] <= 0:
            print("sell price at 0")
            exit()
        if config[name]["stop_loss_price"] <= 0:
            print("stop loss price at 0")
            exit()
        if config[name]["stop_loss_price"] > config[name]["buy_price"]:
            print("stop loss > buy")
            exit()
        if config[name]["buy_price"] > config[name]["signal_buy_price"]:
            print("buy price > signal buy")
            exit()
        if config[name]["signal_buy"] > config[name]["sell_price"]:
            print("signal buy > sell price")
            exit()
    return config

def get_btc_equivalent(balances):
    btc_amount,btc_equivalent = 0,0
    for name in balances:
        if name == "BTC":
            btc_amount = balances[name]
            btc_equivalent += btc_amount
        else:
            btc_equivalent += balances[name]*current_prices[name]
    return btc_amount,btc_equivalent

def main_loop():
    config = load_config()
    buy_orders = {}
    sell_orders = {}
    i = 0
    number_moneys = 2
    balances = {}
    while True:
        #recherche de stop loss, vend si un seuil de sécurité est dépassé
        for name in list(balances):
            if balances[name] == 0:
                continue
            if current_prices[name] < config[name]["stop_loss_price"]:
                trading_api.sell_now(name,sellOrders[name])
                del sellOrders[name]
        #vérifier les ordres d'achats en attente
        if i >= 10:
            i = 0
            if len(buy_orders) > 0:
                orderNumbers = [order["orderNumber"] for order in trading_api.pol.returnOpenOrders("all")]
                for orderNumber in list(buy_orders):
                    if not orderNumber in orderNumbers:
                        #the order is fullfiled,place a sell order
                        balances = trading_api.pol.returnBalances()
                        name,expiration_date = buy_orders[ordeNumber]
                        amount = balances[name]
                        if amount > 0:
                            orderSell = trading_api.place_sell_order(name,amount,config[name]["sell_price"])
                            sell_orders[name] = orderSell
                        del buy_orders[orderNumber]
                for orderNumber in list(buy_orders):
                    (name,expiration_date) = buy_orders[orderNumber]
                    if time.time() > expiration_date:
                        #remove the order
                        trading_api.pol.cancel("BTC_"+name,orderNumber)
                        balances = trading_api.pol.returnBalances()
                        amount = balances[name]
                        if amount > 0:
                            orderSell = trading_api.place_sell_order(name,amount,config[name]["sell_price"])
                            sell_orders[name] = orderSell
                        del buy_orders[orderNumber]
        #regarder les monnaies à acheter
        for name in list(config):
            if balances[name] == 0 and not name in [name for name,expiration_date in buy_orders]):
                if current_prices[name] < config[name]["signal_buy_price"]:
                    balances = trading_api.pol.returnBalances()
                    btc_amount,btc_equivalent = get_btc_equivalent(balances)
                    invest_money = min(btc_equivalent/number_moneys,btc_amount)
                    if invest_money > 0:
                        buy_order_number = trading_api.place_buy_order(invest_money,name,config[name]["buy_price"])
                        buy_order[buy_order_name] = (name,time.time()+5*60)
        i += 1
        time.sleep(1)

if __name__ == "__main__":
    #init()
    main_loop()
