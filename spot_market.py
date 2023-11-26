import requests
from shared_data import *


# whole list of spot markets
def spot_markets_list():
    return requests.request('GET', host + prefix + spot_currency_pairs_url, headers=headers).json()

