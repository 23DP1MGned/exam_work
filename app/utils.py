import requests
import os

class CryptoConvert:
    API_URLS = {
        "BTC": "https://api.binance.com/api/v3/ticker/price?symbol=BTCUSDT",
        "ETH": "https://api.binance.com/api/v3/ticker/price?symbol=ETHUSDT",
        "SOL": "https://api.binance.com/api/v3/ticker/price?symbol=SOLUSDT",
        "DOT": "https://api.binance.com/api/v3/ticker/price?symbol=DOTUSDT",
        "TON": "https://api.binance.com/api/v3/ticker/price?symbol=TONUSDT",
        "DOGE": "https://api.binance.com/api/v3/ticker/price?symbol=DOGEUSDT",
        "LTC": "https://api.binance.com/api/v3/ticker/price?symbol=LTCUSDT",
        "XRP": "https://api.binance.com/api/v3/ticker/price?symbol=XRPUSDT",
        "ADA": "https://api.binance.com/api/v3/ticker/price?symbol=ADAUSDT",
        "AVAX": "https://api.binance.com/api/v3/ticker/price?symbol=AVAXUSDT"
    }

    @staticmethod
    def crypto_rate(crypto):
        url = CryptoConvert.API_URLS.get(crypto.upper())
        if not url:
            print("Error: Unsupported cryptocurrency!")
            return 0.0
        
        try:
            response = requests.get(url)
            data = response.json()
           # print("API Response:", data)
            return float(data.get("price", 0.0))
        except Exception as e:
            print(f"Error getting rate: {e}")
            return 0.0
        
def clear_console():
    os.system("cls" if os.name == "nt" else "clear")

