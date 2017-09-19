#! /usr/bin/python3 
import crypto
import numpy as np

def compute_buy_line(money,n):
    #first, get all the moves from the average in percents
    tab = [money["low"][i]/money["average"][i] for i in range(n)]
    period = 20
    tab2 = [min(tab[i:min(i+period,len(tab))]) for i in range(0,len(tab),period)]
    tab3 = np.sort(tab2)
    if len(tab3) > 10:
        return tab3[10]
    else:
        return 1

def compute_buy_lines(money):
    period = 10
    buy_line = []
    for i in range(0,len(money["average"]),period):
        c = compute_buy_line(money,i)
        for j in range(i,min(len(money["average"]),i+period)):
            buy_line.append(c)
    return buy_line

def compute_move(money,take_profit,stop_loss):
    n = len(money["close"])
    move = [-5]*n
    sell_up = []
    sell_down = []
    for i in range(n):
        low = money["low"][i]
        high = money["high"][i]
        while len(sell_down) > 0 and sell_down[-1][0] >= low:
            ind = sell_down[-1][1]
            if move[ind] == -5:
                move[ind] = -1
            del sell_down[-1]
        while len(sell_up) > 0 and sell_up[0][0] <= high:
            ind = sell_up[0][1]
            if move[ind] == -5:
                move[ind] = 1
            del sell_up[0]
        price = money["open"][i]
        price_take_profit = (1+take_profit/100)*price
        price_stop_loss = (1-stop_loss/100)*price
        #inser price up
        ind = crypto.find_index(sell_up,price_take_profit)
        sell_up.insert(ind,(price_take_profit,i))
        #inser price down
        ind = crypto.find_index(sell_down,price_stop_loss)
        sell_down.insert(ind,(price_stop_loss,i))
    for i in range(n):
        if move[i] == -5:
            move[i] = 0
    money["move"] = move

def stat_up(money):
    n_up = 0
    n = 0
    move = money["move"]
    for i in range(len(move)):
        if move[i] == 1:
            n_up += 1
            n += 1
        elif move[i] == -1:
            n += 1
    print("stat up : ",n_up/n*100)

def stat_up_rsi(money,down,up):
    n_up = 0
    n = 0
    move = money["move"]
    for i in range(len(move)):
        if money["rsi"][i] < up and money["rsi"][i] > down:
            if move[i] == 1:
                n_up += 1
                n += 1
            elif move[i] == -1:
                n += 1
    if n > 0:
        print(down," < RSI < ",up)
        print(n)
        print("stat up : ",n_up/n*100)

def stat_up_change24h(money,down,up):
    n_up = 0
    n = 0
    move = money["move"]
    for i in range(len(move)):
        if money["change_24h"][i] < up and money["change_24h"][i] > down:
            if move[i] == 1:
                n_up += 1
                n += 1
            elif move[i] == -1:
                n += 1
    if n > 0:
        print(down," < change 24h < ",up)
        print(n)
        print("stat up : ",n_up/n*100)

def max_round(p):
    return (p//50) * 50

def value_dollars(btc_holds,p):
    return sum([p*btc for btc in btc_holds])

def market_maker(money):
    m = money["high"][0]
    r = max_round(m)
    buy_points_x = []
    buy_points_y = []
    sell_points_x = []
    sell_points_y = []
    holds = []
    btc_holds = []
    dollars = 300
    invest = 10
    dollars_L = []
    for i in range(len(money["close"])):
        v = dollars + value_dollars(btc_holds,money["close"][i])
        dollars_L.append(v)
        #buy
        m = max(money["high"][i],m)
        r = max_round(m)
        buy_p = r
        if len(holds) > 0:
            buy_p = holds[0] - 50
        buy_p -= 50
        if money["low"][i] < buy_p:
            buy_points_x.append(i)
            buy_points_y.append(buy_p)
            holds = [buy_p+50] + holds
            btc_holds = [invest/buy_p] + btc_holds
            dollars -= invest
        #sell
        while 0 < len(holds) and holds[0] < money["high"][i]:
            sell_points_x.append(i)
            sell_points_y.append(holds[0])
            dollars += btc_holds[0]*holds[0]
            holds = holds[1:]
            btc_holds = btc_holds[1:]
    money["dollars"] = dollars_L
    return buy_points_x,buy_points_y,sell_points_x,sell_points_y

def stat_up_macd(money):
    buy_points_x = []
    buy_points_y = []
    sell_points_x = []
    sell_points_y = []
    n_up = 0
    n = 0
    #move = money["move"]
    #for i in range(1,len(move)):
    #    if money["time_macd"][i] > 0:
    #        if money["change_24h"][i] < -10:
    #        #if money["macd_short"][i] >= money["signal_line_short"][i] and money["macd_short"][i-1] <= money["signal_line_short"][i-1]:
    #            buy_points_x.append(i)
    #            buy_points_y.append(money["open"][i])
    #            if move[i] == 1:
    #                n_up += 1
    #                n += 1
    #            elif move[i] == -1:
    #                n += 1
    #if n > 0:
    #    print("macd")
    #    print(n)
    #    print("stat up : ",n_up/n*100)
    ##if True:#money["change_24h"][i] < -10:
    return buy_points_x,buy_points_y,sell_points_x,sell_points_y

