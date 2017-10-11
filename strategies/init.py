#! /usr/bin/python3

import get_data
import load_data
import params

get_data(params.period,params.moneys)
moneys = load_data.load_moneys(params.period,params.training_period,params.moneys)
last_prices,last_b,last_timestamp = manage_portfolio_past(moneys,params.pamr_step)
one_step_pamr(last_prices,last_b)

