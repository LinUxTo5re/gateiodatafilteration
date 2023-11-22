import requests
import pandas as pd
from shared_data import *
from future_market import *
from filter_spot_market import *
from spot_market import *
from datetime import datetime, timedelta


def common_markets_filtering(spot_usdt_tradable_markets, future_ticker_list):
    future_set = set()
    for i in future_ticker_list:
        future_set.add(i['contract'])
    print(f'total future_set: {len(future_set)}')

    spot_set = set()
    for i in spot_usdt_tradable_markets:
        spot_set.add(i['id'])
    print(f'total spot_set: {len(spot_set)}')

    common_market = future_set.intersection(spot_set)
    print(f"Total Common Markets for spot and futures: {len(common_market)}")
    remove_unmatched_markets = future_set - spot_set
    print("removed Unmatched markets:", len(remove_unmatched_markets))

    for i in future_ticker_list:
        if i['contract'] in list(remove_unmatched_markets):
            future_ticker_list.remove(i)
    print(f'total future_ticker_list after removal: {len(future_ticker_list)}')
    return future_ticker_list


def features_selection(future_ticker_list):
    df = pd.DataFrame(future_ticker_list)
    selected_columns = ['contract', 'mark_price', 'volume_24h_quote']
    selected_df = df[selected_columns]

    for column in selected_df.columns:
        try:
            selected_df[column] = selected_df[column].astype(float)
        except ValueError:
            pass

#removed crypto which price is more than $20
    selected_df = selected_df[selected_df['mark_price'] < 20].sort_values(by='volume_24h_quote')
    print(f"total makets (removed future markets- Price > $20): {len(selected_df)}")
#removed crypto which 24 hrs volume is less than 100k

    selected_df = selected_df[selected_df['volume_24h_quote'] > 100000].sort_values(by='volume_24h_quote',
                                                                                    ascending=False)
    print(f'total markets (removed future markets- volume < 100k): {len(selected_df)}')
    selected_df = selected_df.reset_index()

    selected_df = selected_df.drop('index', axis=1)
    return selected_df


"In this fun, will exclude assets with low volume and less percentage change"


def candlestick_data_handle7d(contract):
    query_param = {'contract': f'{contract}', 'interval': '1d',
                   "from": int((datetime.now() - timedelta(days=7)).timestamp()),
                   "to": int(datetime.now().timestamp())}

    future_candlestick_data7d = requests.request('GET', host + prefix + future_candlestick_url, params=query_param,
                                               headers=headers).json()
    future_candlestick_data7d = pd.DataFrame(future_candlestick_data7d)
    future_candlestick_data7d = future_candlestick_data7d.drop(['c', 'o', 'l', 'h','t'], axis=1)

    for column in future_candlestick_data7d.columns:
        try:
            future_candlestick_data7d[column] = future_candlestick_data7d[column].astype(float)
        except ValueError:
            pass

    # future_candlestick_data7d['pct_change'] = future_candlestick_data7d['c'].diff() / future_candlestick_data7d['c'].shift(
    #     1) * 100

    # 100000 is equal to 1.00e+05 (scientific notation)
    return (future_candlestick_data7d['sum'] < 100000).any()

    
"""
In this fun, will exclude assets which may have high/low ask/bid price difference
 or no order executed 
 or less order executed than idel number of orders executed for this asset.
 for example: atleast 5K orders should be executed in that 1 mins.
 """


def candlestick_data_handle1min(contract):
    query_param = {'contract': f'{contract}', 'interval': '1m',
                   "from": int((datetime.now() - timedelta(minutes=5)).timestamp()),
                   "to": int((datetime.now() - timedelta(minutes=1)).timestamp())}

    future_candlestick_data1m = requests.request('GET', host + prefix + future_candlestick_url, params=query_param,
                                               headers=headers).json()
    future_candlestick_data1m.pop()
    future_candlestick_data1m = pd.DataFrame(future_candlestick_data1m)
    future_candlestick_data1m = future_candlestick_data1m.drop(['t', 'o', 'l', 'h','c'], axis=1)
    #remove assets whose volume/sum is zero or less than 100 usdt for 1min tf of  5mins data
    for column in future_candlestick_data1m.columns:
        try:
            future_candlestick_data1m[column] = future_candlestick_data1m[column].astype(float)
        except ValueError:
            pass
    print(future_candlestick_data1m)
    #sum - trading volume for that tf
    return (future_candlestick_data1m['sum'] < 500).any() 


if __name__ == '__main__':
    print('working')
    print(candlestick_data_handle1min('KAS_USDT'))