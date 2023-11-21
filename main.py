import spot_market
import future_market
import filter_future_market
import filter_spot_market
from datetime import datetime

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
    function will handle dtypes of dataframe, reindxing of indexes
    and filter data using volume of asset.
    '''
    selected_df = filter_future_market.features_selection(common_future_spot_markets)

    '''
    here we're performing deep filtering using contracts candlesticks data
    '''
    print(f'total asset of dataframe (before): {len(selected_df)}')
    for i in selected_df['contract']:
        if filter_future_market.candlestick_data_handle(i):
            selected_df = selected_df[selected_df['contract'] != i]
            print(f"deleted: {i}, remaining assets: {len(selected_df)}")
        else:
            print(f"added: {i}")

    print(f'total asset of dataframe (after): {len(selected_df)}')

    # saving final output of dataframe to Excel file for reference
    selected_df.to_excel(f'final_spot_futures_markets_{datetime.now().strftime("%Y-%m-%d_%H-%M-%S")}.xlsx', index=False)

# Check volatility and filter more coins
# enjoy margin's api and make this product more suitable for your trading. -- to do later, not now
