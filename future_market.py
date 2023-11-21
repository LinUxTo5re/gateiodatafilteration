import requests
from shared_data import *


# whole list of future contracts
# all_future_contracts = requests.request('GET', host + prefix + all_future_contracts_url, headers=headers).json()

# info of single contract
# single_future_contract = requests.request('GET', host + prefix + single_future_contract_url, headers=headers).json()

# whole list of future contract and this will be used in our project
def future_ticker_list():
    return requests.request('GET', host + prefix + future_ticker_list_url, headers=headers).json()
