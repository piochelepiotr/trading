#! /usr/bin/python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jun  6 17:13:53 2017

@author: antoi and piotr
"""
import polo_api
import time

#will modify the order every 30 seconds
retry_period = 0
#will try to buy two times at low price, then, will put a higher price
retry_num = 1
APIKey,Secret = polo_api.get_keys()
pol = polo_api.poloniex(APIKey,Secret)
output_file = "trading_output.data"

def get_btc_amount():
    balances = pol.returnBalances()
    amount = balances['BTC']
    print("amount of bitcoins : ",amount)
    write_output("You have a total of %s bitcoins" % str(amount))
    return amount

def find_rate(pair):
    order_book = pol.returnOrderBook(pair)
    return float(order_book["asks"][0][0]),float(order_book["bids"][0][0])

def buy_low(btc_amount,name,buy_price):
    #place buy order
    pair = "BTC_"+name
    amount = btc_amount / buy_price
    str_amount = '{:0.8f}'.format(amount)
    str_buy_price = '{:0.8f}'.format(buy_price)
    print("buying ",name," at ",str_buy_price)
    ans = pol.buy(pair,str_ratio,str_amount)
    orderNumber = ans["orderNumber"]
    return orderNumber

def place_sell_order(name,amount,price):
    print("placing sell order")
    pair = "BTC_"+name
    str_price = '{:0.8f}'.format(price)
    str_amount = '{:0.8f}'.format(amount)
    print("sell %s %s, rate is %s" % (str_amount,name,str_price))
    print("you will gain ",amount*price," btc")
    print("selling...")
    ans = pol.sell(pair,str_ratio,str_amount)
    print("answer : ",ans)
    return int(ans["orderNumber"])

def sell_now(name,orderNumber):
    print("selling low, stop loss")
    pair = "BTC_"+name
    while(True):
        sell_ratio,buy_ratio = find_rate(pair)
        print("sell ratio = ",sell_ratio)
        print("buy ratio = ",buy_ratio)
        gap = abs((sell_ratio/buy_ratio) - 1)*100
        print("gap is ",gap," %")
        ratio = buy_ratio
        str_ratio = '{:0.8f}'.format(ratio)
        print("modify the order for selling %s, rate is %s" % (name,str_ratio))
        print("you will gain ",amount*ratio," btc")
        print("selling...")
        print("order number : ",orderNumber)
        ans = pol.moveOrder(orderNumber,str_ratio)
        print(ans)
        if ans["success"] == 0:
            #has already been sold
            break
        else:
            #hasn't sold it entirely
            orderNumber = ans["orderNumber"]

def write_output(text):
    date = time.strftime('%d %B %Y %H:%M')
    with open(output_file,"a") as f:
        f.write(date + " : " +text + '\n')

