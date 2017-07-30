#! /usr/bin/python3

import time
import requests
import json
import csv
import os
import multiprocessing

currency_list = ['AMP','ARDR','BCN','BCY','BELA','BLK','BTCD','BTM','BTS','BURST','CLAM','DASH','DCR','DGB','DOGE','EMC2','ETC','ETH','EXP','FCT','FLDC','FLO','GAME','GNO','GNT','GRC','HUC','LBC','LSK','LTC','MAID','NAUT','NAV','NEOS','NMC','NOTE','NXC','NXT','OMNI','PASC','PINK','POT','PPC','RADS','REP','RIC','SBD','SC','SJCX','STEEM','STR','STRAT','SYS','VIA','VRC','VTC','XBC','XCP','XEM','XMR','XPM','XRP','XVC','ZEC']

base_url = "https://poloniex.com/public?command=returnChartData&currencyPair=BTC_"
data_folder = "data"

period = 3600*24*365
step = 3600*24*30*2

def make_dir(path):
    """
    Creates folder if it doesn't exist
    
    Args:
        path: place where the folder must be created
    """
    if(not os.path.isdir(path)):
        os.mkdir(path)

def get_missing_period(name):
    """
    Finds the period of time between the last update of a csv and the current time. 
    
    Args:
        name (string): name of the csv to consider
    
    Returns:
        (int): starting time of the missing period
        (int): end time of the missing period
    """
    end_time = int(time.time())
    start_time = end_time - period
    filename = data_folder + os.sep + name + '.csv'
    exists = os.path.exists(filename)
    if not exists:
        create_csv(name)
    time_ = get_last_timestamp(name)
    if time_ != -1:
        start_time = time_
    return start_time,end_time

def get_last_timestamp(name):
    """
    Finds the last timestamp of a given csv
    
    Args:
        name (string): name of the csv to consider
    
    Returns:
        (int): last timestamp of the csv
    """
    filename = data_folder + os.sep + name + '.csv'
    tp = -1
    with open(filename, 'r') as csvfile:
        reader = csv.reader(csvfile)
        first = True
        for row in reader:
            if first:
                first = False
            else:
                tp = int(row[0])
        return tp
    print("error opening file ",filename)

def create_csv(name):
    """
    Create csv files with headers for every given currency.
    
    Args:
        name (string): name of the csv to consider
    """
    filename = data_folder + os.sep + name + '.csv'
    #permission = input('This operation will delete all previous data,\nAre you sure you want to continue ?\
    #        \nType delete to continue\n')
    #if(permission != "delete"):
    #    return

    make_dir(data_folder)
    with open(filename, 'w') as csvfile:
        columns = ['date','high','low','open', 'close', 'volume', 'quoteVolume', 'weightedAverage']
        wr = csv.writer(csvfile,lineterminator = '\n' )
        wr.writerow(columns)
    print("Data has been deleted")

def get_pair(name):
    """
    Appends missing data until today to a csv by finding the missing period
    
    Args:
        name (string): name of the csv to consider
    """
    print("*******  Getting ", name)
    start_time,end_time = get_missing_period(name)
    while(start_time <= end_time):
        print("start time = ", start_time)
        if(not(get_part_pair(name, start_time+1,start_time + step))):
            return
        start_time += step

def get_part_pair(name, start_time, end_time):
    """
    Appends data from missing period to a csv
    
    Args:
        name (string): name of the csv to consider
        start_time (int): beginning of the missing period
        end_time (int): end of the missing period
        
    Returns:
        (bool) status of the update. False if the update couldn't be made. True otherwise.
    """
    print("start time = ",start_time)
    print("end time = ",end_time)
    url = base_url + name
    url += "&start=" + str(start_time)
    url += "&end=" + str(end_time)
    url += "&period=300"
    r = requests.get(url)
    worked = True
    if(r.status_code != 200):
        worked = False
    else:
        trades_data = json.loads(r.text)
        try:
            error = trades_data['error']
            print("error : ", error)
            worked = False
        except:
            pass
    if(worked):
        data = json.loads(r.text)
        write_data(data, name)
        return True
    else:
        print("impossible to get ", name)
        return False

def write_data(data, name):
    """
    Write the data from the dictionary to the concerned csv files

    Args:
        data: dictionary associating currencies' acronyms to the relevant data
        name: name of the csv to consider
    """
    filename = data_folder + os.sep + name + '.csv'
    with open(filename, 'a') as csvfile:
        wr = csv.writer(csvfile,lineterminator = '\n' )
        for x in data:
            if x['date'] != 0:
                L=[]
                L.append(x['date'])
                L.append(x['high'])
                L.append(x['low'])
                L.append(x['open'])
                L.append(x['close'])
                L.append(x['volume'])
                L.append(x['quoteVolume'])
                L.append(x['weightedAverage'])
                wr.writerow(L)

def refresh_data():
    #p_list = []
    for name in currency_list:
        get_pair(name)
        #p = multiprocessing.Process(target=get_pair,args=(name,))
        #p_list.append(p)
        #p.start()
    #for name in currency_list:
    #    p.join()


