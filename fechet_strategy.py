

# -----------------
# import modules
# -----------------
import requests
import pandas as pd
import json
import datetime as dt
import os
import time

import numpy as np

from pycoingecko import CoinGeckoAPI

from telethon.sync import TelegramClient
from telethon.tl.functions.messages import (GetHistoryRequest)
from telethon.tl.types import (PeerChannel)
from telethon.sync import TelegramClient

import config
from fechet_function import fechet_dist

from sklearn import datasets, linear_model
from sklearn.metrics import mean_squared_error, r2_score



# config
cg = CoinGeckoAPI()
url = 'https://api.coingecko.com/api/v3/search/trending'


# ----------------
# Functions
# ----------------

# connect telegram
def connect_tg():

    client = TelegramClient(config.phone, config.api_id, config.api_hash)

    return client


def send_message(value):

    channel_api = 'bot'+ config.api_messages
    chat_id = config.chat_id_messages
    url = 'https://api.telegram.org/'+channel_api+'/sendMessage?chat_id=-'+chat_id+'&text="{}"'.format(value)
    requests.get(url)


def get_price(token):

    price = cg.get_price([token],['USD'])[token]['usd']

    return price


def scale(value,min,max):
    value_scaled = (value - min) / (max - min)
    return value_scaled

def scale_pattern(Pattern,min,max):
   Pattern_scaled = Pattern
   for i in range(0,len(Pattern)):
        value = (Pattern[i])[1]
        value_scaled = scale(value,min,max)
        (Pattern_scaled[i])[1] = value_scaled
   return Pattern_scaled


def scale_list(list):
    max = np.max(list)
    min = np.min(list)
    list_scaled = np.array([(x - min) / (max - min) for x in list])
    return list_scaled


def scale_range(list,new_min,new_max):

    max = np.max(list)
    min = np.min(list)
    list_scaled_range = np.array([((x - min) / (max - min)) * (new_max - new_min) + new_min for x in list])
    return list_scaled_range


def list_format(list):

     list_formatted = []

     for i in range(0,len(list)):

        tuple = [i,list[i]]

        list_formatted.append(tuple)

     return list_formatted



def main():

    client = connect_tg()
    client.connect()


    pattern = [8,8,8,8,8,9]

    pattern_formatted = list_format(pattern)

    mew_min = np.min(pattern)
    mew_max = np.max(pattern)


    send_message('Connection ok: \n Tracking pattern begins')

    price_list = []
    dist = 100

    while True:


        price = get_price('million')
        price_list.append(price)

        if len(price_list)>=len(pattern):
            price_pattern = price_list[-len(pattern):]

            price_scaled = scale_range(price_pattern,mew_min,mew_max)

            price_formatted = list_format(price_scaled)

            dist = fechet_dist(pattern_formatted, price_formatted)

        if dist<10:
            send_text = 'Pattern Detected!: \n Similarity: ' + str(dist)
            send_message(send_text)

        time.sleep(10)


if __name__ == "__main__":
    main()











