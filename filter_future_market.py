import pandas as pd
from spot_market import *
from datetime import datetime, timedelta
import pytz


def common_markets_filtering(spot_usdt_tradable_markets, future_ticker_list):
    future_set = set()
    for i in future_ticker_list:
        future_set.add(i['contract'])

    spot_set = set()
    for i in spot_usdt_tradable_markets:
        spot_set.add(i['id'])

    common_market = future_set.intersection(spot_set)
    remove_unmatched_markets = future_set - spot_set

    for i in future_ticker_list:
        if i['contract'] in list(remove_unmatched_markets):
            future_ticker_list.remove(i)
    return future_ticker_list


def features_selection(future_ticker_list):
    df = pd.DataFrame(future_ticker_list)
    selected_columns = ['contract', 'mark_price', 'volume_24h_quote']
    selected_df = df[selected_columns]

    for column in selected_df.columns:
        try:
            selected_df.loc[:, column] = selected_df[column].astype(float)
        except ValueError:
            pass
    # removed crypto which price is more than $5
    selected_df = selected_df[selected_df['mark_price'] < 5].sort_values(by='volume_24h_quote')
    # removed crypto which 24 hrs volume is less than 300k

    selected_df = selected_df[selected_df['volume_24h_quote'] > 350000].sort_values(by='volume_24h_quote',
                                                                                    ascending=False)
    selected_df = selected_df.reset_index()

    selected_df = selected_df.drop('index', axis=1)
    return selected_df


"In this fun, will exclude assets with low volume and less percentage change"


def candlestick_data_handle7d(contract):
    ist_timezone = pytz.timezone('Asia/Kolkata')
    ist_now = datetime.now(ist_timezone)
    from_timestamp = int((ist_now - timedelta(days=7)).timestamp())
    to_timestamp = int(ist_now.timestamp())

    query_param = {
        'contract': contract,
        'interval': '1d',
        'from': from_timestamp,
        'to': to_timestamp
    }

    future_candlestick_data7d = requests.request('GET', host + prefix + future_candlestick_url, params=query_param,
                                                 headers=headers).json()
    future_candlestick_data7d = pd.DataFrame(future_candlestick_data7d)
    future_candlestick_data7d = future_candlestick_data7d.drop(['c', 'o', 'l', 'h', 't'], axis=1)

    for column in future_candlestick_data7d.columns:
        try:
            future_candlestick_data7d[column] = future_candlestick_data7d[column].astype(float)
        except ValueError:
            pass

    # 100000 is equal to 1.00e+05 (scientific notation)
    return (future_candlestick_data7d['sum'] < 350000).any()


"""
In this fun, will exclude assets which may have high/low ask/bid price difference
 or no order executed 
 or less order executed than ideal number of orders executed for this asset.
 for example: atleast 5K orders should be executed in that 1 mins.
 """


def candlestick_data_handleofmin(contract, interval, start_min):
    ist_timezone = pytz.timezone('Asia/Kolkata')
    ist_now = datetime.now(ist_timezone)
    from_timestamp = int((ist_now - timedelta(minutes=start_min)).timestamp())
    to_timestamp = int((ist_now - timedelta(minutes=1)).timestamp())

    query_param = {
        'contract': contract,
        'interval': interval,
        'from': from_timestamp,
        'to': to_timestamp
    }

    future_candlestick_data_of_m = requests.request('GET', host + prefix + future_candlestick_url, params=query_param,
                                                    headers=headers).json()
    future_candlestick_data_of_m.pop()
    future_candlestick_data_of_m = pd.DataFrame(future_candlestick_data_of_m)
    future_candlestick_data_of_m = future_candlestick_data_of_m.drop(['t', 'o', 'l', 'h', 'c'], axis=1)
    # remove assets whose volume/sum is zero or less than 100 usdt for 3min/5min tf of  5mins/25mins data
    for column in future_candlestick_data_of_m.columns:
        try:
            future_candlestick_data_of_m[column] = future_candlestick_data_of_m[column].astype(float)
        except ValueError:
            pass
    # sum - trading volume for that tf
    if interval == '5m':
        return (future_candlestick_data_of_m['sum'] < 2500).any()
    else:
        return (future_candlestick_data_of_m['sum'] < 1000).any()
