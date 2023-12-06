import requests
import json
from Config import keys


class APIException(Exception):
    pass


class Crypta:
    @staticmethod
    def get_price(base: str, quote: str, amount: str):
        if quote == base:
            raise APIException(f'Your entered and needed currencies are the same: {base}.')
        if float(amount) <= 0.00:
            raise APIException(f'The currency amount should be greater then 0.00')

        try:
            base = keys[base.upper()]
        except KeyError:
            raise APIException(f'The currency you have entered is not available: {base}')
        try:
            quote = keys[quote.upper()]
        except KeyError:
            raise APIException(f'The currency you have entered is not available: {quote}')
        try:
            your_cur = keys[base]
        except KeyError:
            raise APIException(f'The currency you have entered is not available: {base}')
        try:
            need_cur = keys[quote]
        except KeyError:
            raise APIException(f'The currency you need is not available: {quote}')
        try:
            amount = float(amount)
        except ValueError:
            raise APIException(f'The currency amount should be the number (format: 0.00)')

        r = requests.get(f'https://min-api.cryptocompare.com/data/price?fsym={your_cur}&tsyms={need_cur}')
        total = json.loads(r.content)
        total_base = round(float(total[list(total.keys())[0]])*amount, 2)
        return total_base
