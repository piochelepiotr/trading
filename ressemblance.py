#! /usr/bin/python3

#I used this file only for tests, to test if the algorithm performs better on moneys that have opposit moves

def ressemblance(money1,money2,period):
    n = len(money1['close'])
    r = 0
    t = 0
    for i in range(period,n,period):
        diff1 = money1['close'][i] - money1['close'][i-period]
        diff2 = money2['close'][i] - money2['close'][i-period]
        if diff1*diff2 >= 0:
            r += 1
        t += 1
    return r/t*100

def ressemblances(moneys,period):
    r = {}
    for name in moneys:
        r[name] = {}
        for name2 in moneys:
            r[name][name2] = ressemblance(moneys[name],moneys[name2],period)
            print(name," vs ",name2," : ",r[name][name2])
    return r
