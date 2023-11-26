from shared_data import crypto_price_change_url
import requests


def filter_coins(contract):
    api_url = crypto_price_change_url + '/' + contract
    response = requests.get(api_url)

    if response.status_code == 200:
        if abs(float(response.json()['percentChange'])) > 2:
            return float(response.json()['percentChange'])

