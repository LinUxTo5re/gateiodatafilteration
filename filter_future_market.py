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
    selected_columns = ['contract','mark_price', 'volume_24h_quote']
    selected_df = df[selected_columns]

    for column in selected_df.columns:
        try:
            selected_df[column] = selected_df[column].astype(float)
        except ValueError:
            pass 

    selected_df = selected_df[selected_df['mark_price'] < 20].sort_values(by='volume_24h_quote')

    selected_df = selected_df[selected_df['volume_24h_quote'] > 100000].sort_values(by='volume_24h_quote',ascending=False)
    selected_df = selected_df.reset_index()

    selected_df  = selected_df.drop('index', axis=1)
    return selected_df


"In this fun, will exclude assets with low volume and less percentage change"
def candlestick_data_handle(contract):
    query_param = {'contract':f'{contract}','interval':'1d',
               "from": int((datetime.now() - timedelta(days=7)).timestamp()), 
               "to": int(datetime.now().timestamp())}
    
    future_candlestick_data = requests.request('GET', host + prefix + future_candlestick_url, params = query_param, headers=headers).json()
    future_candlestick_data = pd.DataFrame(future_candlestick_data)
    future_candlestick_data  = future_candlestick_data.drop(['t','o','l','h'], axis=1)

    for column in future_candlestick_data.columns:
        try:
            future_candlestick_data[column] = future_candlestick_data[column].astype(float)
        except ValueError:
            pass  

    future_candlestick_data['pct_change'] = future_candlestick_data['c'].diff() / future_candlestick_data['c'].shift(1) * 100

    #100000 is equal to 1.00e+05 (scientific notation)
    return True if (future_candlestick_data['sum'] < 100000).any() or (future_candlestick_data['v'] < 100000).any() else False
    # if can_delete :
    #     selected_df = selected_df[selected_df['contract'] != contract]
    #     return False
    # else:
    #     return True
