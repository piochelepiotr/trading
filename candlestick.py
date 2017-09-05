#! /usr/bin/python3


##steps

#is it a big move or not ?

def compute_buy_points(data):
    buy_x = []
    buy_y = []
    n = len(data["high"])
    number_down = 0
    for i in range(n):
        if number_down >= 2 and data["open"][i] < data["close"][i-1] and data["close"][i] > data["open"][i-1]:
            buy_x.append(i)
            buy_y.append(data["close"][i])
        if data["close"][i] < data["open"][i]:
            number_down += 1
        else:
            number_down = 0
    return buy_x,buy_y

def compute_change(prices,period):
    n = len(prices)
    changes = []
    for i in range(n):
        old = max(0,i-period)
        changes.append((prices[i] - prices[old])/prices[old])
    return changes

def choose_best(data,i):
    name_min = ""
    mini = 0
    for x in data:
        if name_min == "" or data[x]["change_1h"][i] < mini:
            name_min = x
            mini = data[x]["change_1h"][i]
    return name_min


