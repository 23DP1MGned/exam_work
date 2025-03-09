import json
import os
from app.utils import CryptoConvert

SUPPORTED_CRYPTOS = ["BTC", "ETH", "SOL", "DOT", "TON", "DOGE", "LTC", "XRP", "ADA", "AVAX"]

class CryptoWallet:
    def __init__(self, filename):
        self.filename = filename
        self.balances = {"USDT": 0.0, **{crypto: 0.0 for crypto in SUPPORTED_CRYPTOS}}
        self.load_wallet()
    
    def load_wallet(self):
        if os.path.exists(self.filename):
            with open(self.filename, "r") as file:
                self.balances = json.load(file)
    
    def save_wallet(self):
        with open(self.filename, "w") as file:
            json.dump(self.balances, file, indent=4)
    
    def total_balance(self):
        total_usd = self.balances["USDT"]
        for crypto, amount in self.balances.items():
            if crypto != "USDT" and amount > 0:
                total_usd += amount * CryptoConvert.crypto_rate(crypto)
        print(f"Overall balance: {total_usd:.2f} USD")

    
    def top_up(self, amount):
        self.balances["USDT"] += amount
        self.save_wallet()
        print(f"The balance is replenished by {amount:.2f} USDT")
    
    def usdt_to_crypto(self, crypto, amount):
        if crypto not in SUPPORTED_CRYPTOS:
            print("Error: Unsupported cryptocurrency!")
            return
        if amount > self.balances["USDT"]:
            print("Error: Insufficient funds!")
            return
        rate = CryptoConvert.crypto_rate(crypto)
        crypto_amount = amount / rate
        self.balances["USDT"] -= amount
        self.balances[crypto] += crypto_amount
        self.save_wallet()
        print(f"Converted: {amount:.2f} USDT -> {crypto_amount:.8f} {crypto}")

    
    def crypto_to_usdt(self, crypto, amount):
        if crypto not in SUPPORTED_CRYPTOS:
            print("Error: Unsupported cryptocurrency!")
            return
        if amount > self.balances[crypto]:
            print("Error: Insufficient funds!")
            return
        rate = CryptoConvert.crypto_rate(crypto)
        if rate == 0:
            print("Error: Failed to get exchange rate!")
            return
        usdt_amount = amount * rate
        self.balances[crypto] -= amount
        self.balances["USDT"] += usdt_amount
        self.save_wallet()
        print(f"Converted: {amount:.8f} {crypto} -> {usdt_amount:.2f} USDT")