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
print("waiting_time is :",last_timestamp + params.waiting_time - time.time())
#buy all the moneys, check if you only have BTC
#while(True):
#one_step_pamr(last_prices,last_b)

