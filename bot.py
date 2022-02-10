import requests
import json
import numpy as np
from time import time, sleep
from pushbullet import Pushbullet

puburl = 'https://poloniex.com/public?command=returnTicker'
cur_value = 0

API_KEY = "o.ezhuUGocJYE3hBhrbo3tPFkIL38XCa8p"
pb = Pushbullet(API_KEY)

bullmarket = 1

price_his = np.array(96)
price_buffer = np.array(96)

price_his = np.zeros(96)
price_buffer = np.zeros(96)

ma10_ar = np.array(8)
ma10_buf = np.array(8)

ma10_ar = np.zeros(8)
ma10_buf = np.zeros(8)


exma_ar = np.array(5)
exma_buf = np.array(5)

exma_ar = np.zeros(5)
exma_buf = np.zeros(5)


exma = 0
ma10 = 0


def pull_cur_data():
    global cur_value
    r=requests.get(puburl)
    binary = r.content
    result = json.loads(binary)
    print("ID:"+ str(result["USDT_XRP"]["id"]))
    cur_value=float(result["USDT_XRP"]["last"])
    print("current value in USDT:"+str(cur_value))

def ref_arr():
    global price_his
    global price_buffer
    i = 0
    for i in range(95):
        price_buffer[i] = price_his[i+1]

    price_his = price_buffer
    price_his[95] = cur_value

    print(price_his)

def cal_avr():
    global ma10_ar
    global exma_ar
    global ma10_buf
    global exma_buf
    global ma10
    global exma

    # ma10 ###
    ma_sum = 0;
    for i in range(7):
        ma_sum = ma_sum + price_his[85+i]

    ma10 = ma_sum/8
    for i in range(7):
        ma10_buf[i] = ma10_ar[i+1]

    ma10_ar = ma10_buf
    ma10_ar[7] = ma10

    #######################

    #exp_ma_avr

    sf = 2/(1+exma_ar.size)
    exma = (cur_value * sf) + (exma_ar[4]*(1-sf))

    for i in range(4):
        exma_buf[i] = exma_ar[i+1]

    exma_ar = exma_buf
    exma_ar[4] = exma

    ###############

def bull_check():
    global exma
    global ma10

    if exma > ma10:
        return 1
    else:
        return 0

def buy_check():
    global bullmarket
    print(bull_check())
    print(bullmarket)
    if bull_check() != bullmarket:

        print("bullmarket afterwards")
        print(bullmarket)
        if bull_check() == 1:
            buy()
        else:
            sell()
    bullmarket = bull_check()



def buy():
    print("buy")
    pb.push_note('XRPBULL', 'buy')

def sell():
    print("sell nigga")
    pb.push_note('XRPBULL', 'sell')

while True:
    sleep(10 - time() % 10)
	# thing to run
    pull_cur_data()
    print("###########")
    ref_arr()
    print("###########")
    cal_avr()
    print("###########")
    buy_check()
    print("###########")
