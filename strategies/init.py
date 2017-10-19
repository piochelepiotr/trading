#! /usr/bin/python3

import get_data
import load_data
import params
import time
import pamr
import trade_algorithms

#trade_algorithms.display_prices()
#trade_algorithms.display_holdings()
#trade_algorithms.place_buy_order("ETH",0.0003,100)
#trade_algorithms.move_buy_order(357948230611,0.0004,"ETH")
#trade_algorithms.place_sell_order("LTC",0.012,0.14513888)
#trade_algorithms.move_sell_order("25217839100",0.00065)
#trade_algorithms.cancel_orders()
#trade_algorithms.sell_moneys({"LTC":-1})
#print(trade_algorithms.pol.returnOpenOrders("all"))


get_data.get_data(params.period,params.moneys)
moneys = load_data.load_moneys(params.period,params.training_period,params.moneys)
last_prices,last_b,last_timestamp = pamr.manage_portfolio_past(moneys,params.pamr_step)
print("current time : ",time.time())
print("last timestamp : ",last_timestamp)
print("difference : ",time.time() - last_timestamp)
wait = last_timestamp + params.waiting_time - time.time()
print("waiting_time is :",wait)
time.sleep(max(0,wait))
#check if you only have BTC
holdings = trade_algorithms.pol.returnBalances()
for name in holdings:
    if holdings[name] != 0:
        print("you have ",holdings[name]," of ",name)
        if name != "BTC":
            exit()
btc_hold = holdings["BTC"]
#save time
next_time = time.time()+params.waiting_time
#compute change since last time
x,last_prices = trade_algorithms.compute_change(last_prices)
#get new b
b = pamr.compute_portfolio(last_b,x)
#buy all the moneys
trade_algorithms.buy_moneys({name:b[name]*btc_hold for name in b})
while(True):
    #get holdings
    holdings,btc = trade_algorithms.get_important_holdings(params.moneys)
    total_not_btc = sum(list(holdings.values()))
    #sleep to the right time
    time.sleep(max(0,next_time-time.time()))
    #save time
    next_time = time.time()+params.waiting_time
    #get new prices and changes
    x,last_prices = trade_algorithms.compute_change(last_prices)
    #compute new b
    b = pamr.compute_portfolio(b,x)
    #compute the amounts we need to get
    prev_b = {name:holdings[name] / total_not_btc for name in holdings}
    amounts_diff,t = pamr.compute_amounts(prev_b,b,holdings,last_prices)
    sell_moneys = {}
    buy_moneys = {}
    tot_buy = 0
    for name in amounts_diff:
        if amounts_diff[name] <= -0.00015:
            sell_moneys[name] = -amounts_diff[name]
        else if amounts_diff[name] >= 0.00015:
            buy_moneys[name] = amounts_diff[name]
            tot_buy += buy_moneys[name]
    #sell moneys
    trade_algorithms.sell_moneys(sell_moneys)
    #get btc_amount
    holdings,btc = trade_algorithms.get_important_holdings(params.moneys)
    #buy moneys
    buy_moneys = {name : buy_moneys[name] * btc / tot_buy for name in buy_moneys}
    trade_algorithms.buy_moneys(moneys)

