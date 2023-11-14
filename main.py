# import telebot
# from telebot import types
# import time
# import ccxt

# bot = telebot.TeleBot('6944341639:AAHVIrqTCyhCJYdbnR3TU0WEiTOhtSXpbW8')


import requests
import pandas as pd
import time

# List of available exchange platforms
PLATFORMS_API = {
    'Bybit': 'https://api.bybit.com/spot/quote/v1/ticker/price',
    'Binance': 'https://api.binance.com/api/v3/ticker/price',
    'Bitget': 'https://api.bitget.com/api/v2/spot/market/tickers'
}

SYMBOLS_API = 'https://api.huobi.pro/v1/common/currencys'


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


def normalize(custom_dictionary, key_price='price', key_symbol='symbol'):
    return {
        'price': custom_dictionary[key_price],
        'symbol': custom_dictionary[key_symbol]
    }


def get_data(url):
    try:
        response = requests.get(url)
        return response.json()
    except Exception as e:
        print(f"Error fetching data from {e}")


def get_symbols_data():
    try:
        data = get_data(SYMBOLS_API)
        local_symbols = []
        for local_symbol in data['data'][1:]:
            local_symbols.append(local_symbol.upper() + "USDT")
        return local_symbols
    except Exception as e:
        print(f"Error fetching symbols data from {e}")


def get_platform_data(exchange, local_symbol):
    try:
        url = PLATFORMS_API[exchange] + '?symbol=' + local_symbol
        return get_data(url)
    except Exception as e:
        print(f"Error fetching platform data from {e}")


def get_ticker_data(exchange, local_symbol):
    try:
        data = get_platform_data(exchange, local_symbol)
        # print(exchange,local_symbol, data)
        if exchange == 'Binance' and ('symbol' in data):
            return normalize(data)
        elif exchange == 'Bybit' and data['ret_code'] == 0:
            return normalize(data['result'])
        elif exchange == 'Bitget' and data['msg'] == 'success':
            return normalize(data['data'][0], 'lastPr')
        return -1

    except Exception as e:
        print(f"Error fetching data from {exchange}: {e}")


while True:
    try:
        symbols = get_symbols_data()
        # print(symbols)
        for symbol in symbols:
            price_comparison = {}
            for platform in PLATFORMS_API:
                ticker_data = get_ticker_data(platform, symbol)
                if ticker_data != -1:
                    price_comparison[platform] = ticker_data
            result_comparison = custom_comparison(price_comparison, 'price')
            # print(f"Price Comparison fn: {result_comparison}")
            print(f"{symbol} Price Comparison: {result_comparison}")
            # print(f"{symbol} Price Comparison: {price_comparison}")
        time.sleep(10)
    except KeyboardInterrupt:
        print("\nExiting...")
        break
