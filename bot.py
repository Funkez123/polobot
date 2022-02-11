import requests
import json
import numpy as np
from time import time, sleep
from pushbullet import Pushbullet
import hashlib
import hmac
from poloniex import Poloniex
import poloniex

puburl = 'https://poloniex.com/public?command=returnTicker'
cur_value = 0
lowest_ask = 0
highest_bid = 0
balance_XRP = 0
balance_USDT = 0
Key = 'G67353F1-COBNCY7Z-MLN7LVN3-1LQ0U2PX'
Secret='69ff7fad0e0786e99dda4ce4d9cbe9526a7e7eaa819fc51950ce516cb73a0f754598eb67432635bc9e2fed7f327a49f8f0c68bcf39e77bd47f1d66d6d2cadbf0'

polo = poloniex.Poloniex(key=Key, secret=Secret)

API_KEY = "o.ezhuUGocJYE3hBhrbo3tPFkIL38XCa8p"
pb = Pushbullet(API_KEY)

bullmarket = 1

price_his = np.array(96)
price_buffer = np.array(96)

price_his = np.zeros(96)
price_buffer = np.zeros(96)

ma10_ar = np.array(9)
ma10_buf = np.array(9)

ma10_ar = np.zeros(9)
ma10_buf = np.zeros(9)


exma_ar = np.array(6)
exma_buf = np.array(6)

exma_ar = np.zeros(6)
exma_buf = np.zeros(6)


exma = 0
ma10 = 0


def pull_cur_data():
    global cur_value
    global highest_bid
    global lowest_ask
    r=requests.get(puburl)
    binary = r.content
    result = json.loads(binary)
    #print("ID:"+ str(result["USDT_XRP"]["id"]))
    cur_value=float(result["USDT_XRP"]["last"])
    print("current value in USDT:"+str(cur_value))
    lowest_ask=float(result["USDT_XRP"]["lowestAsk"])
    highest_bid=float(result["USDT_XRP"]["highestBid"])


def ref_arr():
    global price_his
    global price_buffer
    i = 0
    for i in range(95):
        price_buffer[i] = price_his[i+1]

    price_his = price_buffer
    price_his[95] = cur_value

    #print(price_his)

def cal_avr():
    global ma10_ar
    global exma_ar
    global ma10_buf
    global exma_buf
    global ma10
    global exma

    # ma10 ###
    ma_sum = 0;
    for i in range(exma_ar.size-1):
        ma_sum = ma_sum + price_his[85+i]

    ma10 = ma_sum/exma_ar.size
    for i in range(exma_ar.size-1):
        ma10_buf[i] = ma10_ar[i+1]

    ma10_ar = ma10_buf
    ma10_ar[exma_ar.size-1] = ma10

    #######################

    #exp_ma_avr

    sf = 2/(1+exma_ar.size)
    exma = (cur_value * sf) + (exma_ar[exma_ar.size-1]*(1-sf))

    for i in range(exma_ar.size-1):
        exma_buf[i] = exma_ar[i+1]

    exma_ar = exma_buf
    exma_ar[exma_ar.size-1] = exma

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
    print(__________)
    if bull_check() == 1:
        print('Bullmarket')
    else:
        print('Bearmarket')
    print(__________)

    if bull_check() != bullmarket:

#        print("bullmarket afterwards")
#        print(bullmarket)
        if bull_check() == 1:
            buy()
        else:
            sell()
    bullmarket = bull_check()



def buy():
    print("buy")
    pb.push_note('XRP', 'buy')
    polobuy()
def sell():
    print("sell nigga")
    pb.push_note('XRP', 'sell')

def polobuy():
    ordernum = polo.buy(currencyPair='USDT_XRP',rate=(lowest_ask-(lowest_ask*0.001)),amount=round(1.3/cur_value))
    pb.push_note('XRP', 'gekauft')

def polosell():
    ordernum = polo.sell(currencyPair='USDT_XRP',rate=(highest_bid+(highest_bid*0.001)),amount=balance_XRP)
    pb.push_note('XRP', 'verkauft')
def balance_check():
    balance = polo.returnBalances()
    print('_____________')
    print("Balance")
    print("XRP:" + str(balance['XRP']))
    global balance_XRP
    balance_XRP = float(balance['XRP'])
    print("USDT:"+str(balance['USDT']))
    global balance_USDT
    balance_USDT = float(balance['USDT'])
    print('_____________')
    bal = float(balance['XRP'])
    print('total value of XRP: ' + str(bal*cur_value))
    print('________________________')

while True:
    sleep(60*2 - time() % 60*2)
	# thing to run

    balance_check()
    pull_cur_data()

    print("__________")
    ref_arr() #refresh arrays

    cal_avr()  ## calculate averages

    buy_check()  ##buycheck
    print('Iteration done')
    print('______')
    print('')
    print('')
    print('')
