#shared data
host = "https://api.gateio.ws"
prefix = "/api/v4"
headers = {'Accept': 'application/json', 'Content-Type': 'application/json'}
settle = 'usdt' #btc
spot_ticker_info_url = '/spot/tickers'
spot_currency_pairs_url = '/spot/currency_pairs'
all_future_contracts_url = f'/futures/{settle}/contracts'
single_future_contract_url = f'/futures/{settle}/contracts/BTC_USDT'
future_ticker_list_url = f'/futures/{settle}/tickers'
future_candlestick_url = '/futures/usdt/candlesticks'