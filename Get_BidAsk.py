# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""
import cbpro
import krakenex
import datetime as dt
import pandas as pd
import requests
import os


def average_of_list(l):
    t=0
    for s in l:
        try:
            t+=s
        except:
            t+=float(s)
    return t/len(l)



#READ_DATABASE
path = "C://Users//Bernardo Figueiredo//OneDrive//Área de Trabalho//DADOS_Bid_Ask_BTC.xlsx" #Botar caminho pro arquivo com // separando

df_coinbase = pd.read_excel(path, index_col=0, sheet_name = 'Coinbase')
df_kraken = pd.read_excel(path, index_col=0, sheet_name = 'Kraken')
df_binance = pd.read_excel(path, index_col=0, sheet_name = 'Binance')
df_gemini = pd.read_excel(path, index_col=0, sheet_name = 'Gemini')


date_time = dt.datetime.now()

#COINBASE
public_client_coinbase = cbpro.PublicClient()
bids_cb, asks_cb = [], []

#KRAKEN
kraken = krakenex.API()
bids_kr, asks_kr = [], []

#BINANCE
bids_bin, asks_bin = [], []

#GEMINI
bids_gem, asks_gem = [], []


for number_tries in range(10):
    
    #COINBASE
    order_book_cb = public_client_coinbase.get_product_order_book('BTC-USD', level=1)
    print('Coinbase', order_book_cb)
    bids_cb.append(float(order_book_cb['bids'][0][0]))
    asks_cb.append(float(order_book_cb['asks'][0][0]))
    
    #KRAKEN
    order_book_kr = kraken.query_public('Depth', {'pair':'XXBTZUSD', 'count':'1'})['result']['XXBTZUSD']
    bids_kr.append(order_book_kr['bids'][0][0])
    asks_kr.append(order_book_kr['asks'][0][0])
        
    #BINANCE
    resp_binance = requests.get('https://api.binance.com/api/v3/depth?symbol=BTCUSDT').json()
    bids_bin.append(resp_binance['bids'][0][0])
    asks_bin.append(resp_binance['asks'][0][0])
    
    
    #GEMINI
    resp_gem = requests.get('https://api.gemini.com/v1/book/btcusd').json()
    bids_gem.append(resp_gem['bids'][0]['price'])
    asks_gem.append(resp_gem['asks'][0]['price'])
    #print('\nGEMINI',resp_gem)

bid_cb , ask_cb = average_of_list(bids_cb), average_of_list(asks_cb)
bid_kr, ask_kr = average_of_list(bids_kr), average_of_list(asks_kr)
bid_bin, ask_bin = average_of_list(bids_bin), average_of_list(asks_bin)
bid_gem, ask_gem = average_of_list(bids_gem), average_of_list(asks_gem)

print('COINBASE: Bid {} - Ask {}'.format(bid_cb , ask_cb))
print('KRAKEN: Bid {} - Ask {}'.format(bid_kr, ask_kr))
print('BINANCE: Bid {} - Ask {}'.format(bid_bin, ask_bin))
print('GEMINI: Bid {} - Ask {}'.format(bid_gem, ask_gem))


df_coinbase[date_time] = {'Bid': bid_cb, 'Ask': ask_cb, 'Bid-Ask Spread': ask_cb-bid_cb}
