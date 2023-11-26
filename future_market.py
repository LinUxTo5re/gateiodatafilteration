import requests
from shared_data import *


# whole list of future contract and this will be used in our project
def future_ticker_list():
    return requests.request('GET', host + prefix + future_ticker_list_url, headers=headers).json()
