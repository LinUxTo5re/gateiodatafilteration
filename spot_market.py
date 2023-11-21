import requests
from shared_data import *


# whole list of spot markets
def spot_markets_list():
    return requests.request('GET', host + prefix + spot_currency_pairs_url, headers=headers).json()


# not usable code
# --------------------------------------------------------------------------------------------------
'''
url = '/spot/tickers'
query_param = {"currency_pair":"BTC_USDT"}
spot_ticker_info = requests.request('GET', host + prefix + url, headers=headers,params = query_param).json()
len(spot_ticker_info)
'''

'''
spot ticker info for specific 
crypto asset
'''


def spot_ticker_info(ticker='BTC_USDT'):
    query_param = {"currency_pair": f"{ticker}"}
    return requests.request('GET', host + prefix + spot_ticker_info_url, headers=headers, params=query_param).json()[0]
# ------------------------------------------------------------------------------------------------------------
