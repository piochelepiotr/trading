#! /usr/bin/python3
# -*- coding: utf-8 -*-

import requests
import socket
from unittest.mock import patch
import os
import ssl
from requests_toolbelt import SSLAdapter

#s = requests.Session()
#s.mount('https://',SSLAdapter(ssl.PROTOCOL_TLSv1))
#ret = s.get("https://93.184.216.34", headers={"Host": "example.org"})
#r = s.get("https://poloniex.com/public?command=returnTicker",headers={'host':'poloniex.com'})
#print(r)
ret = requests.get("https://poloniex.com/public?command=returnTicker")
print(ret)

#host = socket.gethostbyname("poloniex.com")
#print(host)
#url = 'http://{}/public?command=returnTicker'.format(host)
#ret = requests.get(url,headers= { 'Host':'poloniex.com'})
#print(ret)
#request = urllib2.Request('https://{}/path'.format(host),headers = {'Host': 'poloniex.com'})
#page = urllib2.urlopen(request)

