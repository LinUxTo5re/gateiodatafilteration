import spot_market
import future_market
import filter_future_market
import filter_spot_market
from datetime import datetime
import os
import glob
import filter_dataframe

# entry pt of my code
if __name__ == '__main__':
    # list of available spot markets on gate io
    spot_markets_list = spot_market.spot_markets_list()

    # list of available future markets on gate io
    future_ticker_list = future_market.future_ticker_list()

    '''
    list of spot markets which have USDT
    as quote and are tradable in current time
    '''
    spot_usdt_tradable_markets = filter_spot_market.spot_usdt_tradable_markets(spot_markets_list)

    '''
    function will return list of common markets from spot and future.
    it'll also remove unwanted markets which are not same.    
    '''
    common_future_spot_markets = filter_future_market.common_markets_filtering(spot_usdt_tradable_markets,
                                                                               future_ticker_list)

    '''
    function will handle dtypes of dataframe, reindexing of indexes
    and filter data using volume of asset.
    '''
    selected_df = filter_future_market.features_selection(common_future_spot_markets)

    '''
    here we're performing deep filtering using contracts candlesticks data for 7d
    '''
    print(f'total asset of dataframe-candlesticks (before): {len(selected_df)}')
    for i in selected_df['contract']:
        if filter_future_market.candlestick_data_handle7d(i):
            selected_df = selected_df[selected_df['contract'] != i]
            print(f"deleted: {i}, remaining assets (7d): {len(selected_df)}")
        else:
            if filter_future_market.candlestick_data_handleofmin(i, '5m', 25):
                selected_df = selected_df[selected_df['contract'] != i]
                print(f"deleted: {i}, remaining assets (5min): {len(selected_df)}")
            else:
                if filter_future_market.candlestick_data_handleofmin(i, '3m', 6):
                    selected_df = selected_df[selected_df['contract'] != i]
                    print(f"deleted: {i}, remaining assets (3min): {len(selected_df)}")
                else:
                    print(f"added: {i}")  # finally added

    print(f'total asset of dataframe-candlesticks (after): {len(selected_df)}')

    # Check if there are any XLS files, then delete them
    if glob.glob(os.path.join(os.getcwd(), '*.xlsx')):
        for file in glob.glob(os.path.join(os.getcwd(), '*.xlsx')):
            os.remove(file)

    # filtered coins with volume 500k or more
    selected_df = selected_df[selected_df['volume_24h_quote'] > 500000].sort_values(by='volume_24h_quote',
                                                                                    ascending=False)
    try:
        print(f'total crypto before price change(): ', len(selected_df))
        for crypto in selected_df['contract']:
            if not filter_dataframe.filter_coins(crypto):
                selected_df = selected_df[selected_df['contract'] != crypto]

        selected_df = selected_df.sort_values(by='volume_24h_quote', ascending=False)
        print(f'total crypto after price change(): ', len(selected_df))
    except Exception as e:
        pass
    # Saving XLSX file
    selected_df.to_excel(f'final_spot_futures_markets_{datetime.now().strftime("%Y-%m-%d_%H-%M-%S")}.xlsx', index=False)
