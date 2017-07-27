#! /usr/bin/python3
import pandas as pd 
import matplotlib.pyplot as plt

period = 3600*24*30*4//300
long_period = 3600*24*30*6//300


#12,26,9
step = 600//300
short_term   = 1*step
macd_short_term    = 12*step
macd_long_term    = 26*step
macd_term    = 9*step
vol_term     = 20*step
vol_term2    = 40*step
fee          = 0.25/100
min_period = 3600//300
level = 20
var_min = 0
period_sell = 24*3*3600//300
sell_limit = 1
sell_limit_down = 3
keep_period = 0//300

currency_list = ['ETH','GNT','PASC','AMP','ARDR','BCN','BCY','BELA','BLK','BTCD','BTM','BTS','BURST','CLAM','DASH','DCR','DGB','DOGE','EMC2','ETC','EXP','FCT','FLDC','FLO','GAME','GRC','HUC','LBC','LSK','LTC','MAID','NAUT','NAV','NEOS','NMC','NOTE','NXC','NXT','OMNI','PINK','POT','PPC','RADS','REP','RIC','SBD','SC','SJCX','STEEM','STR','STRAT','SYS','VIA','VRC','VTC','XBC','XCP','XEM','XMR','XPM','XRP','XVC','ZEC']

def ema(data,n):
    #(1-lamb)^n = 0.5
    lamb = 1-pow(0.5,1/n)
    ema=data[0]
    emas=[]
    for p in data:
        ema = (1-lamb)*ema + lamb*p
        emas.append(ema)
    return emas

def average(data,n):
    av = []
    L = [data[0]]*n
    s = sum(L)
    for i in data:
        s -= L[0]
        L = L[1:]
        L.append(i)
        s += i
        av.append(s/n)
    return av

def compute_diff(L1,L2):
    return [L1[i] - L2[i] for i in range(len(L1))]

def intersections(L1,L2):
    inter = []
    L = compute_diff(L1,L2)
    for i in range(1,len(L)):
        if L[i-1]*L[i] <= 0:
            inter.append(i)
    return inter

def find_next_buy(price,var,start):
    for i in range(start,len(price)):
        mini = min(price[i-min_period:i])
        maxi = max(price[i-min_period:i])
        dist_min = 100*(price[i]-mini)/(maxi-mini)
        varia = 100*(maxi-mini)/maxi
        if dist_min < level and var[i] > 0 and varia > var_min:
            return i
    return -1

def find_next_sell(price,momentum,ema_momentum,start):
    buy_p = price[start]
    #conditions to sell :
    #drop to much
    #cross 
    crosses = intersections(momentum,ema_momentum)
    for i in range(start+keep_period,len(price)):
        var = 100*(price[i]-buy_p)/buy_p
        if var < -sell_limit_down:
            print("loss")
            return i
        if var > sell_limit:
        #if i in crosses and momentum[i] < ema_momentum[i]:
            #print("win")
            return i
    #if start+keep_period < len(price):
    #    return start+keep_period
    return -1

def trade(price,var,momentum,ema_momentum):
    price = price               [-period:]
    var = var                   [-period:]
    momentum = momentum         [-period:]
    ema_momentum = ema_momentum [-period:]

    buy_points = []
    sell_points = []
    buy_inter_x  = []
    buy_inter_y  = []
    sell_inter_x = []
    sell_inter_y = []

    i = min_period
    up = 0
    tot = 0
    money = 1
    while True:
        i = find_next_buy(price,var,i)
        if i == -1:
            break
        buy_inter_x.append(i)
        buy_inter_y.append(price[i])
        buy_p = price[i]
        i = find_next_sell(price,momentum,ema_momentum,i)
        if i == -1:
            break
        sell_inter_x.append(i)
        sell_inter_y.append(price[i])
        if price[i] >= buy_p:
            up += 1
        money = money / buy_p * price[i]
        tot += 1
    if tot != 0:
        print("The proportion is ",100*up/tot)
        print("money at the end is ",money)
    return buy_inter_x,buy_inter_y,sell_inter_x,sell_inter_y

def derivate(L,scale=False):
    d = []
    if scale:
        d = [(L[i] - L[i-1])/L[i] for i in range(len(L))]
    else:
        d = [(L[i] - L[i-1]) for i in range(len(L))]
    d[0] = 0
    return d

def test_cur(name,disp=False):
    df = pd.read_csv("../final/data/"+name+".csv")
    
    price= df['close'].values[-long_period:]
    short_ema = ema(price,short_term)
    macd_short_ema = ema(price,macd_short_term)
    macd_long_ema = ema(price,macd_long_term)
    macd = compute_diff(macd_short_ema,macd_long_ema)
    signal = ema(macd,macd_term)
    deriv = derivate(short_ema)
    momentum = compute_diff(macd,signal)
    ema_momentum = ema(momentum,macd_term)
    buy_inter_x,buy_inter_y,sell_inter_x,sell_inter_y = trade(price,deriv,momentum,ema_momentum)

    print("name = ",name," and len = ",len(price))
    
    if  disp and len(buy_inter_x) > 0:
        f, axarr = plt.subplots(3, sharex=True)
        axarr[0].set_title(name)
        axarr[0].plot(price       [-period:])
        axarr[0].plot(short_ema   [-period:])
        axarr[0].plot(buy_inter_x,buy_inter_y,'go',color='red')
        axarr[0].plot(sell_inter_x,sell_inter_y,'go',color='purple')
        axarr[1].plot(macd       [-period:])
        axarr[1].plot(signal       [-period:])
        axarr[2].plot(momentum       [-period:])
        axarr[2].plot(ema_momentum       [-period:])
        plt.show()

for x in currency_list:
    test_cur(x,True)

#test_cur("BLK",True)

