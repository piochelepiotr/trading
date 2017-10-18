import polo_api
import time
APIKey,Secret = polo_api.get_keys()
pol = polo_api.poloniex(APIKey,Secret)

def place_buy_order(name,price,btc_amount):
    if btc_amount < 0.00015:
        print("amount to low, must be at least 0.00015 btc, not buying ",name)
    pair = "BTC_"+name
    amount = btc_amount / price
    str_amount = '{:0.8f}'.format(amount)
    str_price = '{:0.8f}'.format(price)
    print("buy %s %s, rate is %s" % (str_amount,name,str_price))
    print("you will use ",btc_amount," btc")
    ans = input("Type ok to continue")
    if ans != "ok":
        print("not buying")
        exit()
    ans = pol.buy(pair,str_price,str_amount)
    print(ans)
    if "error" in ans:
        if ans["error"] == "Not enough BTC.":
            print("not enought btc, changing amount")
            time.sleep(1)
            holdings = pol.returnBalances()
            print(holdings)
            place_buy_order(name,price,holdings["BTC"])

#not finished !!!!!!!!!
def move_buy_order(num,price):
    str_price = '{:0.8f}'.format(price)
    print("moving order ",num," to price ",price)
    ans = input("Type ok to continue")
    if ans != "ok":
        print("not buying")
        exit()
    ans = pol.moveOrder(num,str_price)
    print(ans)
    if "error" in ans:
        if ans["error"] == "Not enough BTC.":
            print("not enought btc, changing amount")
            time.sleep(1)
            holdings = pol.returnBalances()
            print(holdings)
            place_buy_order(name,price,holdings["BTC"])

def place_sell_order(name,price,amount):
    pair = "BTC_"+name
    str_amount = '{:0.8f}'.format(amount)
    str_price = '{:0.8f}'.format(price)
    print("selling %s %s, rate is %s" % (str_amount,name,str_price))
    print("you will gain ",amount*price," btc")
    ans = input("Type ok to continue")
    if ans != "ok":
        print("not selling")
        exit()
    ans = pol.sell(pair,str_price,str_amount)
    print(ans)

def move_sell_order(num,price):
    pair = "BTC_"+name
    str_price = '{:0.8f}'.format(price)
    print("moving order num ",num," to price ", price)
    ans = input("Type ok to continue")
    if ans != "ok":
        print("not moving order")
        exit()
    ans = pol.moveOrder(num,str_price)
    print(ans)

def change_sell_orders(price_ref):
    ticker = pol.returnTicker()
    openOrders = pol.returnOpenOrders()
    print("open orders : ",openOrders)
    n = 0
    for pair in openOrders:
        for order in openOrders[pair]:
            n += 1
            if order["type"] != "sell":
                print("error, not sell order")
                exit()
            move_sell_order(order["orderNumber"],ticker[pair][price_ref])
    if n == 0:
        return True
    else:
        return False

def change_buy_orders(price_ref):
    ticker = pol.returnTicker()
    openOrders = pol.returnOpenOrders()
    print("open orders : ",openOrders)
    n = 0
    for pair in openOrders:
        for order in openOrders[pair]:
            n += 1
            if order["type"] != "buy":
                print("error, not buy order")
                exit()
            move_sell_order(order["orderNumber"],ticker[pair][price_ref])
    if n == 0:
        return True
    else:
        return False

def sell_moneys(moneys):
    #quantities are in btc
    #get what you've got
    holdings = pol.returnBalances()
    #sell everything
    if moneys is None:
        moneys = {}
        for name in holdings:
            if holdings[name] != 0:
                moneys[name] = -1
    #get ticker
    ticker = pol.returnTicker()
    #place all the orders
    for name in money:
        pair = "BTC_" + name
        quantity = holdings[name]
        if moneys[name] != -1:
            quantity = min(moneys[name]/float(ticker[pair]["last"]),holdings[name])
        place_sell_order(name,float(ticker[pair]["lowestAsk"]),quantity)
    time.sleep(5)
    #check if there are still here, if yes, moves them : does that mutltiple times
    for i in range(5):
        if change_sell_orders("lowerAsk"):
            print("SOLD EVERYTHING")
            return
        time.sleep(5)
    #moves at a lower price : should sell immediatly (check after one second for instance)
    for i in range(100):
        if change_sell_orders("highestBid"):
            print("SOLD EVERYTHING")
            return
        time.sleep(1)
    print("ERROR : enable to sell money, why ?")

def buy_moneys(moneys):
    #quantities are in btc
    #get what you've got ? (how many btc for instance)
    holdings = pol.returnBalances()
    #get ticker
    ticker = pol.returnTicker()
    total_btc_spent = sum(list(moneys.values()))
    btc_hold = holdings["BTC"]
    #place all the orders
    for name in money:
        pair = "BTC_" + name
        btc_quantity = moneys[name] * btc_hold / total_btc_spent
        quantity = btc_quantity / ticker[pair]["lowerAsk"]
        place_buy_order(name,float(ticker[pair]["highestBid"]),quantity)
    time.sleep(5)
    #check if there are still here, if yes, moves them : does that mutltiple times
    for i in range(5):
        if change_buy_orders("highestBid"):
            print("BOUGHT EVERYTHING")
            return
        time.sleep(5)
    #moves at a higher price : should buy immediatly (check after one second for instance)
    for i in range(100):
        if change_buy_orders("lowerAsk"):
            print("BOUGHT EVERYTHING")
            return
        time.sleep(1)
    print("ERROR : enable to sell money, why ?")

def compute_change(last_prices):
    ticker = pol.returnTicker()
    x = {name : ticker["BTC_"+name]["last"]/last_prices[name] for name in last_prices}
    prices = {name : ticker["BTC_"+name]["last"] for name in last_prices}
    return x,prices
