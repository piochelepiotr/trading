#! /usr/bin/python3

currencies = ['AMP','ARDR','BCN','BCY','BELA','BLK','BTCD','BTM','BTS','BURST','CLAM','DASH','DCR','DGB','DOGE','ETC','ETH','EXP','FCT','FLDC','FLO','GAME','GNO','GNT','GRC','HUC','LBC','LSK','LTC','MAID','NAUT','NAV','NEOS','NMC','NOTE','NXC','NXT','OMNI','PASC','PINK','POT','PPC','RADS','REP','RIC','SBD','SC','SJCX','STEEM','STR','STRAT','SYS','VIA','VRC','VTC','XBC','XCP','XEM','XMR','XPM','XRP','XVC','ZEC']
period = 300
#moneys = ["SYS","XMR","STRAT","EXP","ETH","XRP"]#currencies[0:10]
#moneys = currencies[0:20]
moneys = ["ETH","DASH","ZEC","XMR","BTCD","GNO","LTC","XBC","DCR","OMNI"]
training_period = 3600*24*7
waiting_time = 3*300
pamr_step = waiting_time//period
