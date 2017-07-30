#! /usr/bin/python3

import requests
import json

url = "https://poloniex.com/public?command=returnTicker"
r = requests.get(url)
ticker = json.loads(r.text)
names = {}
for name in ticker:
    names[ticker[name]["id"]] = name
print(names)
