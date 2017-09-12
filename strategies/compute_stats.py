#! /usr/bin/python3

import crypto

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

def stat_up_macd(money):
    n_up = 0
    n = 0
    move = money["move"]
    for i in range(1,len(move)):
        if money["macd"][i] >= money["signal_line"][i] and money["macd"][i-1] <= money["signal_line"][i-1]:
            if move[i] == 1:
                n_up += 1
                n += 1
            elif move[i] == -1:
                n += 1
    if n > 0:
        print("macd")
        print(n)
        print("stat up : ",n_up/n*100)

