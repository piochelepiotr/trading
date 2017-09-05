#! /usr/bin/python3
# -*- coding: utf-8 -*-

import requests
import socket
from unittest.mock import patch
import os

#ret = requests.get("https://poloniex.com/public?command=returnTicker")

host = socket.gethostbyname("poloniex.com")
print(host)
url = 'http://{}/public?command=returnTicker'.format(host)
ret = requests.get(url,headers= { 'Host':'poloniex.com'})
print(ret)
request = urllib2.Request('https://{}/path'.format(host),headers = {'Host': 'poloniex.com'})
#page = urllib2.urlopen(request)

