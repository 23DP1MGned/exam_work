import requests

API_URL = "https://api.coingecko.com/api/v3/simple/price?ids=bitcoin&vs_currencies=eur,usd"

class CryptoConvert:
    @staticmethod
    def get_btc_exchange_rate(currency):
        response = requests.get(API_URL)
        data = response.json()
        return data["bitcoin"][currency]
