#! /usr/bin/python3

import websocket
import time
import json
import multiprocessing

def on_message(ws, message):
    print(message)

def on_error(ws, error):
    print(error)

def on_close(ws):
    print("### closed ###")

def on_open(ws):
    print("ONOPEN")
    def run(*args):
        #ws.send(json.dumps({'command':'subscribe','channel':1001}))
        ws.send(json.dumps({'command':'subscribe','channel':1002}))
        #ws.send(json.dumps({'command':'subscribe','channel':1003}))
        #ws.send(json.dumps({'command':'subscribe','channel':'BTC_XMR'}))
        while True:
            time.sleep(1)
        ws.close()
        print("thread terminating...")
    multiprocessing.Process(target=run,args=()).start()

if __name__ == "__main__":
    websocket.enableTrace(True)
    ws = websocket.WebSocketApp("wss://api2.poloniex.com/",
                              on_message = on_message,
                              on_error = on_error,
                              on_close = on_close)
    ws.on_open = on_open
    ws.run_forever()
