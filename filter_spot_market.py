def spot_usdt_tradable_markets(spot_markets_list):
    return [i for i in spot_markets_list
            if i['trade_status'] == 'tradable' and i['quote'] == 'USDT']
