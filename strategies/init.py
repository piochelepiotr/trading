#! /usr/bin/python3

import get_data
import load_data
import params
import time
import pamr



get_data.get_data(params.period,params.moneys)
moneys = load_data.load_moneys(params.period,params.training_period,params.moneys)
last_prices,last_b,last_timestamp = pamr.manage_portfolio_past(moneys,params.pamr_step)
print("current time : ",time.time())
print("last timestamp : ",last_timestamp)
print("difference : ",time.time() - last_timestamp)
wait = last_timestamp + params.waiting_time - time.time()
print("waiting_time is :",wait)
time.sleep(max(0,wait))
#compute change since last time
#get new b, function ?
#check if you only have BTC
#buy all the moneys
while(True):
    #get holdings
    #sleep to the right time
    #get current prices
    #save time
    #compute the amounts we need to get
    #sell moneys
    #get btc_amount
    #buy moneys

