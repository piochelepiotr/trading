#! /usr/bin/python3

import numpy as np

#combien a varié x par rapport à y
def change(x,y):
    return (x/y - 1)*100

def find_best_money(moneys,i):
    name_min = list(moneys)[0]
    mini = moneys[name_min]['change_24h'][i]
    for name in moneys:
        if moneys[name]['change_24h'][i] < mini:
            mini = moneys[name]['change_24h'][i]
            name_min = name
    return name_min

def choose_buy_points2(moneys):
    n = len(moneys[list(moneys)[0]]['close'])
    buy_points_x = {}
    buy_points_y = {}
    for name in moneys:
        print(name)
        buy_points_x[name] = []
        buy_points_y[name] = []
    for i in range(n):
        name = find_best_money(moneys,i)
        buy_points_x[name].append(i)
        buy_points_y[name].append(moneys[name]['close'][i])
    return buy_points_x,buy_points_y

def choose_buy_points(moneys,period):
    n = len(moneys[list(moneys)[0]]['close'])
    buy_points_x = {}
    buy_points_y = {}
    sell_points_x = {}
    sell_points_y = {}
    for name in moneys:
        buy_points_x[name] = []
        buy_points_y[name] = []
        sell_points_x[name] = []
        sell_points_y[name] = []
    for name in moneys:
        #print(name)
        #m = 0
        for i in range(n):
            #if moneys[name]['macd'][i] >= 0 and moneys[name]['macd'][i] >= moneys[name]['signal_line'][i] and moneys[name]['rsi'][i] < 60:
            if moneys[name]['macd'][i] >= moneys[name]['signal_line'][i] and moneys[name]['macd'][max(0,i-1)] <= moneys[name]['signal_line'][max(0,i-1)]:
                buy_points_x[name].append(i)
                buy_points_y[name].append(moneys[name]['close'][i])
                #if moneys[name]['close'][i] < moneys[name]['close'][min(n-1,i+(3600*2)//300)]:
                #    m += 1
        #if len(buy_points_x) != 0:
        #    print("percent : ",m/len(buy_points_x[name])*100)
    return buy_points_x,buy_points_y,sell_points_x,sell_points_y

def manage_portfolio(moneys,period):
    n = len(moneys[list(moneys)[0]]['close'])
    m = len(moneys)
    buy_points_x = {}
    buy_points_y = {}
    sell_points_x = {}
    sell_points_y = {}
    moneys_amount = {}
    btc_equ_L = []
    b = []
    x = []
    eps = 1
    for name in moneys:
        buy_points_x[name] = []
        buy_points_y[name] = []
        sell_points_x[name] = []
        sell_points_y[name] = []
    for i in range(0,n,period):
        #balance portfolio
        total_btc = 1
        if i > 0:
            total_btc = sum([moneys_amount[name]*moneys[name]['close'][i] for name in moneys])
            x = [moneys[name]['close'][i]/moneys[name]['close'][i-period] for name in moneys]
            x_b = np.dot(x,[1/m]*m)
            diff = [xi - x_b for xi in x]
            to = max(0,(np.dot(b,x) - eps)/np.dot(diff,diff))
            b = [b[j] - to*diff[j] for j in range(m)]
        else:
            b = [1/m]*m
        print("bitcoin : ",total_btc)
        for j,name in enumerate(moneys):
            moneys_amount[name] = (b[j]*total_btc) / moneys[name]['close'][i]
        for j in range(i,min(i+period,n)):
            btc_equ_L.append(total_btc)
    for name in moneys:
        moneys[name]['btc_equ'] = btc_equ_L
    x_tot = [moneys[name]['close'][n-1]/moneys[name]['close'][0] for name in moneys]
    x_b_tot = np.dot(x_tot,[1/m]*m)
    print("var = ",x_b_tot)
    return buy_points_x,buy_points_y,sell_points_x,sell_points_y

def choose_buy_points3(moneys,period):
    n = len(moneys[list(moneys)[0]]['close'])
    buy_points_x = {}
    buy_points_y = {}
    sell_points_x = {}
    sell_points_y = {}
    for name in moneys:
        buy_points_x[name] = []
        buy_points_y[name] = []
        sell_points_x[name] = []
        sell_points_y[name] = []
    sell_orders = [] 
    btc_money = 1
    number_investment = 3
    max_keep = (3600*24*7)//period
    btc_equ_L = []
    for i in range(n):
        #sell what is to be sold
        for ind,(name,price,amount,end,stop_loss) in enumerate(sell_orders):
            #search for gain
            if moneys[name]['high'][i] > price:
                btc_money += (amount*price)*(1-0.0015)
                sell_points_x[name].append(i)
                sell_points_y[name].append(price)
                print("selling ",name," at ",price)
                del sell_orders[ind]
            elif moneys[name]['low'][i] < stop_loss:
                p = moneys[name]['low'][i]
                sell_points_x[name].append(i)
                sell_points_y[name].append(p)
                print("selling ",name," at ",p)
                btc_money += (amount*p)*(1-0.0025)
                del sell_orders[ind]
            #elif i > end:
            #    p = moneys[name]['close'][i]
            #    btc_money += (amount*p)*(1-0.0025)
            #    sell_points_x[name].append(i)
            #    sell_points_y[name].append(p)
            #    print("selling ",name," at ",p)
            #    del sell_orders[ind]
        #get the btc equivalent of our altcoins
        btc_equ = btc_money
        for name,price,amount,end,stop_loss in sell_orders:
            btc_equ += amount*moneys[name]['close'][i]
        btc_equ_L.append(btc_equ)
        if i < (24*3600)//period:
            continue
        #buy new moneys if there are good trades to do
        for name in moneys:
            #if abs(change(moneys[name]['min_week'][i],moneys[name]['close'][i])) < 10 and abs(change(moneys[name]['min_month'][i],moneys[name]['close'][i])) < 20 and abs(change(moneys[name]['max_week'][i],moneys[name]['close'][i])) > 50:
            got_it = False
            for name2,price,amount,end,stop_loss in sell_orders:
                if name2 == name:
                    got_it = True
            if got_it == True:
                continue
            #if abs(change(moneys[name]['min_week'][i],moneys[name]['close'][i])) < 5 and abs(change(moneys[name]['max_week'][i],moneys[name]['close'][i])) > 20:
            current_price = moneys[name]['close'][i]
            middle = moneys[name]['bollinger_middle'][i]
            if current_price < moneys[name]['bollinger_down'][i] and moneys[name]['macd'][i] >= moneys[name]['signal_line'][i]:
                p = moneys[name]['close'][i]
                m = moneys[name]['max_week'][i]
                amount = min(btc_equ/number_investment,btc_money)
                if amount > 0.05:
                    amount_altcoin = amount/p*(1-0.0025)
                    print("buying ",name, " at ",p)
                    buy_points_x[name].append(i)
                    buy_points_y[name].append(p)
                    btc_money -= amount
                    #adding sell orders
                    sell_orders.append((name,middle,amount_altcoin,0,current_price - (middle-current_price)))
                    #sell_orders.append((name,p+(m-p)*0.25,amount_altcoin/3,i+max_keep,p*(1-0.03)))
                    #sell_orders.append((name,p+(m-p)*0.50,amount_altcoin/3,i+max_keep,p*(1-0.03)))
                    #sell_orders.append((name,p+(m-p)*1,amount_altcoin/3,i+max_keep,p*(1-0.03)))
    for name in moneys:
        moneys[name]['btc_equ'] = btc_equ_L
    return buy_points_x,buy_points_y,sell_points_x,sell_points_y
