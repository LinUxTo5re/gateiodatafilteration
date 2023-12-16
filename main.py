import pandas as pd
import spot_market
import future_market
import filter_future_market
import filter_spot_market
import filter_dataframe
from tqdm import tqdm


def run_my_code():
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
    progress_bar_all = tqdm(selected_df['contract'], desc='Processing contracts', total=len(selected_df),
                            colour='green')
    for i in progress_bar_all:
        progress_bar_all.set_postfix({'Processing': i})
        if filter_future_market.candlestick_data_handle7d(i):
            selected_df = selected_df[selected_df['contract'] != i]
        else:
            if filter_future_market.candlestick_data_handleofmin(i, '5m', 26):
                selected_df = selected_df[selected_df['contract'] != i]
            else:
                if filter_future_market.candlestick_data_handleofmin(i, '3m', 10):
                    selected_df = selected_df[selected_df['contract'] != i]

    # filtered coins with volume 500k or more
    selected_df = selected_df[selected_df['volume_24h_quote'] > 500000].sort_values(by='volume_24h_quote',
                                                                                    ascending=False)
    selected_df = selected_df.reset_index()
    selected_df = selected_df.drop('index', axis=1)
    selected_df_bak = selected_df.copy()

    print("\033[97m" + "=" * 87)
    try:
        progress_bar_sort = tqdm(selected_df['contract'].items(), desc='Processing contracts', total=len(selected_df),
                                 colour='green')
        for index, contract in progress_bar_sort:
            try:
                selected_df.at[index, 'no_change_pct_sign'], selected_df.at[
                    index, 'change_pct'] = filter_dataframe.filter_coins(contract)
                progress_bar_sort.set_postfix({'Processing': contract})
            except Exception as e:
                pass

        selected_df.dropna(subset=['no_change_pct_sign'], inplace=True)  # drop row if contain NaN in any column

        selected_df = selected_df.reset_index()
        if len(selected_df) > 5:
            selected_columns = ['contract', 'mark_price', 'volume_24h_quote', 'change_pct', 'no_change_pct_sign']
            sorted_by_volume = selected_df[selected_columns].sort_values(by=['volume_24h_quote'],
                                                                         ascending=[False]).head(5).copy()
            sorted_by_pct_change = selected_df[selected_columns].sort_values(by=['no_change_pct_sign'],
                                                                             ascending=[False]).head(
                5).copy()
            sorted_by_pct_change.drop('no_change_pct_sign', axis=1, inplace=True)
            sorted_by_volume.drop('no_change_pct_sign', axis=1, inplace=True)
            print("\033[91m" + "=" * 87)
            print(f"sorted by volume: \n {sorted_by_volume}")
            print("\033[92m" + "=" * 87)
            print(f"sorted by pct_change: \n {sorted_by_pct_change}")
            print("\033[95m" + "=" * 87)
            print(
                f"common df: \n {pd.merge(sorted_by_volume, sorted_by_pct_change, on=['contract', 'mark_price', 'volume_24h_quote', 'change_pct'], how='inner')}")
        else:
            print("\033[92m" + "=||=" * 25)
            print(f"{selected_df_bak.sort_values(by='volume_24h_quote', ascending=False).head(10)}")
    except Exception as e:
        pass


# block to execute code manually

if __name__ == "__main__":
    run_my_code()
