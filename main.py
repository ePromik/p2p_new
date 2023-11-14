
# import telebot
# from telebot import types
# import time
import ccxt

#bot = telebot.TeleBot('6944341639:AAHVIrqTCyhCJYdbnR3TU0WEiTOhtSXpbW8')



import requests
import pandas as pd
import time

# List of available exchange platforms
platforms = {
    'Bybit': 'https://api.bybit.com/spot/quote/v1/ticker/price',
    'Binance': 'https://api.binance.com/api/v3/ticker/price',
    'Bitget': 'https://api.bitget.com/api/v2/spot/market/tickers'

}


symbols = ['BTCUSDT']

def custom_comparison(dictionares, keyValue):
    results = {}
    for item in dictionares.items():
        place = item[0]
        values = item[1]
        results[place] = {}
        for item_two in dictionares.items():
            place_two = item_two[0]
            values_two = item_two[1]
            if place != place_two:
                results[place][place_two] = 100 - (float(values[keyValue]) / float(values_two[keyValue])) * 100
    return results

# def custom_comparison(dictionares, keyValue):
#     results = {}
#     platforms = list(dictionares.keys())
#     for item in range(len(platforms)):
#         place = platforms[item]
#         values = dictionares[place]
#         results[place] = {}
#         for j in range(item+1, len(platforms)):
#             place_two = platforms[j]
#             values_two = dictionares[place_two]
#             results[place][place_two] = 100 - (float(values[keyValue]) / float(values_two[keyValue])) * 100
#     return results


def get_ticker_data(exchange, symbol):
    try:
        if exchange == 'Binance':
            url = platforms[exchange] + '?symbol=' + symbol
            response = requests.get(url)
            data = response.json()
            return data
        elif exchange == 'Bybit':
            url = platforms[exchange] + '?symbol=' + symbol
            response = requests.get(url)
            data = response.json()
            return data['result']
        elif exchange == 'Bitget':
            url = platforms[exchange] + '?symbol=' + symbol
            response = requests.get(url)
            data = response.json()
            return data['data']
    except Exception as e:
        print(f"Error fetching data from {exchange}: {e}")



while True:
    try:
        for symbol in symbols:
            price_comparison = {}
            for platform in platforms:
                ticker_data = get_ticker_data(platform, symbol)
                price_comparison[platform] = ticker_data
            result_comparison = custom_comparison(price_comparison, 'price')
            #print(f"Price Comparison fn: {result_comparison}")
            print(f"{symbol} Price Comparison: {result_comparison}")
            #print(f"{symbol} Price Comparison: {price_comparison}")
        time.sleep(10) # Wait for 10 seconds before fetching data again
    except KeyboardInterrupt:
        print("\nExiting...")
        break





























# def get_binance_quotes():
#     url = "https://api.binance.com/api/v3/ticker/price"
#     response = requests.get(url)
#     data = response.json()
#     return data
# data = get_binance_quotes()
# print(data)
#
#
# print('-----------------------------------------------------------------------------')
#
# def get_bybit_price():
#     url1 = "https://api.bybit.com/spot/quote/v1/ticker/price"
#     response1 = requests.get(url1)
#     data1 = response1.json()
#     return data1['result'],['price']
# data1 = get_bybit_price()
# print(data1)

# @bot.message_handler(func=lambda message: True)
# def send_bitcoin_price(message):
#     response = requests.get('https://api.binance.com/api/v3/ticker/price?symbol=BTCUSDT')
#     data = response.json()
#     price = data['price']
#     response1 = requests.get('https://api.bybit.com/spot/quote/v1/ticker/price?symbol=BTCUSDT')
#     data1 = response1.json()
#     price1 = data1['result']['price']
#     bot.reply_to(message, f"The current price of Bitcoin on Binance is {price}/{price1}USDT.")
# bot.polling()

