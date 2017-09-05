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
    amount = float(balances['BTC'])
    print("amount of bitcoins : ",amount)
    write_output("You have a total of %s bitcoins" % str(amount))
    return amount

def buy_moneys(money_list):
    n = len(money_list)
    #check whats the amount of bitcoin that we have
    btc = get_btc_amount()
    #divide the amount, we invest the same amount in each money
    #keep a little margin
    for_each = btc/(n+0.05)
    retry_dates = [-1 for i in range(n)]
    orderNumbers = ["" for i in range(n)]
    sold = 0
    try_num = 0
    while sold < n:
        for i,name in enumerate(money_list):
            if retry_dates[i] != -2:
                retry_dates[i],orderNumbers[i] = buy_crypto(name,for_each,try_num,retry_dates[i],orderNumbers[i])
                if retry_dates[i] == -2:
                    print("SOLD ONE CRYPTO")
                    sold += 1
        try_num += 1
    print("everything has been bought")

def find_rate(pair):
    order_book = pol.returnOrderBook(pair)
    return float(order_book["asks"][0][0]),float(order_book["bids"][0][0])

def buy_crypto(name,btc_amount, try_num, retry_date,orderNumber):
    if retry_date == -2:
        return -2,orderNumber
    if retry_date != -1:
        wait_time = retry_date - time.time()
        if wait_time > 0:
            print("waiting for next try")
            time.sleep(wait_time)
    pair = "BTC_"+name
    sell_ratio,buy_ratio = find_rate(pair)
    print("sell ratio = ",sell_ratio)
    print("buy ratio = ",buy_ratio)
    gap = abs((sell_ratio/buy_ratio) - 1)*100
    print("gap is ",gap," %")
    ratio = buy_ratio
    if try_num >= retry_num:
        ratio = sell_ratio
    amount = btc_amount/sell_ratio
    str_amount = '{:0.8f}'.format(amount)
    str_ratio = '{:0.8f}'.format(ratio)
    if try_num == 0:
        print("buy %s %s, rate is %s" % (str_amount,name,str_ratio))
        print("you will use ",btc_amount," btc")
        #ans = input("Type ok to continue")
        #if ans == "ok":
        print("buying...")
        ans = pol.buy(pair,str_ratio,str_amount)
        print(ans)
        orderNumber = ans["orderNumber"]
        return time.time()+retry_period,orderNumber
    else:
        print("modify the order for buying %s of %s, rate is %s" % (str_amount,name,str_ratio))
        print("you will use ",btc_amount," btc")
        print("buying...")
        print("order number : ",orderNumber)
        ans = pol.moveOrder(orderNumber,str_ratio)
        print(ans)
        if ans["success"] == 0:
            #has already been sold
            print("OK************")
            return -2,orderNumber
        else:
            return time.time()+retry_period,ans["orderNumber"]

def sell_crypto(name,amount, try_num, retry_date,orderNumber):
    if retry_date == -2:
        return -2,orderNumber
    if retry_date != -1:
        wait_time = retry_date - time.time()
        if wait_time > 0:
            print("waiting for next try")
            time.sleep(wait_time)
    pair = "BTC_"+name
    sell_ratio,buy_ratio = find_rate(pair)
    print("sell ratio = ",sell_ratio)
    print("buy ratio = ",buy_ratio)
    gap = abs((sell_ratio/buy_ratio) - 1)*100
    print("gap is ",gap," %")
    ratio = sell_ratio
    if try_num >= retry_num:
        ratio = buy_ratio
    str_amount = '{:0.8f}'.format(amount)
    str_ratio = '{:0.8f}'.format(ratio)
    if try_num == 0:
        print("sell %s %s, rate is %s" % (str_amount,name,str_ratio))
        print("you will gain ",amount*ratio," btc")
        print("selling...")
        ans = pol.sell(pair,str_ratio,str_amount)
        print(ans)
        orderNumber = ans["orderNumber"]
        return time.time()+retry_period,orderNumber
    else:
        print("modify the order for selling %s of %s, rate is %s" % (str_amount,name,str_ratio))
        print("you will gain ",amount*ratio," btc")
        print("selling...")
        print("order number : ",orderNumber)
        ans = pol.moveOrder(orderNumber,str_ratio)
        print(ans)
        if ans["success"] == 0:
            #has already been sold
            return -2,orderNumber
        else:
            #hasn't sold it entirely
            return time.time()+retry_period,ans["orderNumber"]

def sell_everything():
    balances = pol.returnBalances()
    names = []
    for i,name in enumerate(list(balances.keys())):
        if float(balances[name]) != 0 and name != 'BTC':
            print(name)
            print(float(balances[name]))
            names.append(name)
    n = len(names)
    retry_dates = [-1 for i in range(n)]
    orderNumbers = ["" for i in range(n)]
    sold = 0
    try_num = 0
    while sold < n:
        for i,name in enumerate(names):
            if retry_dates[i] != -2:
                retry_dates[i],orderNumbers[i] = sell_crypto(name,float(balances[name]),try_num,retry_dates[i],orderNumbers[i])
                if retry_dates[i] == -2:
                    print("SOLD ONE CRYPTO")
                    sold += 1
        try_num += 1
    print("everything has been sold")

def write_output(text):
    date = time.strftime('%d %B %Y %H:%M')
    with open(output_file,"a") as f:
        f.write(date + " : " +text + '\n')

def get_btc_equivalent():
    balances = pol.returnBalances()
    ticker = pol.returnTicker()
    btc_amount = 0
    for i,name in enumerate(list(balances.keys())):
        if float(balances[name]) != 0:
            btc = 0
            if name != 'BTC':
                btc = float(balances[name])*float(ticker["BTC_"+name]["last"])
                print("you have %s of %s that represents %s bitcoins" % (balances[name],name,str(btc)))
            else:
                btc = float(balances[name])
                print("You have %s bitcoins" % str(btc))
            btc_amount += btc
    print("You have a total of %s bitcoins" % str(btc_amount))

get_btc_equivalent()

#sell_everything()

#get_btc_amount()
#buy_moneys(["NMC"])
