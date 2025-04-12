import requests
import os
import time
import re

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

class Color:
    RED = "\033[31m"
    GREEN = "\033[32m"
    YELLOW = "\033[33m"
    BLUE = "\033[34m"
    RESET = "\033[0m"
    PURPLE = "\033[35m"
    GRAY = "\033[90m"


def framed_menu(content: str, width: int = 51) -> str:
        line = f"   {content}"
        if len(line) > width - 2:
            line = line[:width - 5] + "..."
        padded_line = line.ljust(width - 2)
        return f"║{padded_line}║"

def framed_adress(content: str, width: int = 71) -> str:
        def strip_ansi(text): return re.sub(r'\x1B\[[0-?]*[ -/]*[@-~]', '', text)
        line = f"   {content}"
        vis_len = len(strip_ansi(line))

        if vis_len > width - 2:
            trimmed, count, in_ansi = "", 0, False
            for c in line:
                if c == '\033': in_ansi = True
                if not in_ansi: count += 1
                trimmed += c
                if in_ansi and c.isalpha(): in_ansi = False
                if count >= width - 5: break
            line = trimmed + "..."

        pad = " " * (width - 2 - len(strip_ansi(line)))
        return f"║{line}{pad}║"

def framed_transaction(content: str, width: int = 170) -> str:
        def strip_ansi(text): return re.sub(r'\x1B\[[0-?]*[ -/]*[@-~]', '', text)
        line = f"   {content}"
        vis_len = len(strip_ansi(line))

        if vis_len > width - 2:
            trimmed, count, in_ansi = "", 0, False
            for c in line:
                if c == '\033': in_ansi = True
                if not in_ansi: count += 1
                trimmed += c
                if in_ansi and c.isalpha(): in_ansi = False
                if count >= width - 5: break
            line = trimmed + "..."

        pad = " " * (width - 2 - len(strip_ansi(line)))
        return f"║{line}{pad}║"