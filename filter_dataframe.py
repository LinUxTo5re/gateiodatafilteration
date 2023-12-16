from shared_data import crypto_price_change_url
import requests
from numpy import nan


def filter_coins(contract):
    api_url = crypto_price_change_url + '/' + contract
    response = requests.get(api_url)

    if response.status_code == 200:
        percent_change = response.json().get('percentChange')

        if percent_change is not None and abs(float(percent_change)) > 2:
            return abs(float(percent_change)), float(percent_change)
        else:
            return nan, nan
    else:
        return nan, nan
