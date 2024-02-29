# shared data
host = "https://api.gateio.ws"
prefix = "/api/v4"
headers = {'Accept': 'application/json', 'Content-Type': 'application/json'}
settle = 'usdt'  # btc
spot_ticker_info_url = '/spot/tickers'
spot_currency_pairs_url = '/spot/currency_pairs'
all_future_contracts_url = f'/futures/{settle}/contracts'
single_future_contract_url = f'/futures/{settle}/contracts/BTC_USDT'
future_ticker_list_url = f'/futures/{settle}/tickers'
future_candlestick_url = '/futures/usdt/candlesticks'
crypto_price_change_url = f'https://data.gateapi.io/api2/1/ticker'
usdt_price_filter = 5
hrs_24_volume = 350000  # 350k
days_7_volume = 500000  # 500k
min_5_volume = 2500  # 2.5k
min_1_volume = 1000  # 1k
top_markets_default = 10
