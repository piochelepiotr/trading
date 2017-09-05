#! /usr/bin/python3

import time
import requests
import json
import csv
import os
import multiprocessing
import load_data


base_url = "https://poloniex.com/public?command=returnChartData&currencyPair=BTC_"
data_folder_base = "data_"

period = 3600*24*30*3
step = 3600*24*30*2

def make_dir(path):
    """
    Creates folder if it doesn't exist
    
    Args:
        path: place where the folder must be created
    """
    if(not os.path.isdir(path)):
        os.mkdir(path)

def get_missing_period(name,spacing):
    """
    Finds the period of time between the last update of a csv and the current time. 
    
    Args:
        name (string): name of the csv to consider
    
    Returns:
        (int): starting time of the missing period
        (int): end time of the missing period
    """
    data_folder = data_folder_base + str(spacing)
    end_time = int(time.time())
    start_time = end_time - period
    filename = data_folder + os.sep + name + '.csv'
    exists = os.path.exists(filename)
    if not exists:
        create_csv(name,spacing)
    time_ = get_last_timestamp(name,spacing)
    if time_ != -1:
        start_time = time_
    return start_time,end_time

def get_last_timestamp(name,spacing):
    """
    Finds the last timestamp of a given csv
    
    Args:
        name (string): name of the csv to consider
    
    Returns:
        (int): last timestamp of the csv
    """
    data_folder = data_folder_base + str(spacing)
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

def create_csv(name,spacing):
    """
    Create csv files with headers for every given currency.
    
    Args:
        name (string): name of the csv to consider
    """
    data_folder = data_folder_base + str(spacing)
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

def get_pair(name,spacing):
    """
    Appends missing data until today to a csv by finding the missing period
    
    Args:
        name (string): name of the csv to consider
    """
    print("*******  Getting ", name)
    start_time,end_time = get_missing_period(name,spacing)
    while(start_time <= end_time):
        print("start time = ", start_time)
        if(not(get_part_pair(name, start_time+1,start_time + step,spacing))):
            return
        start_time += step

def get_part_pair(name, start_time, end_time,spacing):
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
    url += "&period=" + str(spacing)
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
        write_data(data, name,spacing)
        return True
    else:
        print("impossible to get ", name)
        return False

def write_data(data, name,spacing):
    """
    Write the data from the dictionary to the concerned csv files

    Args:
        data: dictionary associating currencies' acronyms to the relevant data
        name: name of the csv to consider
    """
    data_folder = data_folder_base + str(spacing)
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

def get_data(spacing):
    p_list = []
    for name in load_data.currency_list:
        #get_pair(name,spacing)
        p = multiprocessing.Process(target=get_pair,args=(name,spacing))
        p_list.append(p)
        p.start()
    for name in load_data.currency_list:
        p.join()


get_data(300)

