import json
import os
from app.utils import CryptoConvert
from app.models.Transactions import Transactions

SUPPORTED_CRYPTOS = ["BTC", "ETH", "SOL", "DOT", "TON", "DOGE", "LTC", "XRP", "ADA", "AVAX"]

class CryptoWallet:
    def __init__(self, filename):
        self.filename = filename
        self.balances = {"USDT": 0.0, **{crypto: 0.0 for crypto in SUPPORTED_CRYPTOS}}
        self.load_wallet()
    
    def load_wallet(self):
        if os.path.exists(self.filename):
            try:
                with open(self.filename, "r") as file:
                    data = json.load(file)

                    if "USDT" not in data:
                        data["USDT"] = 0.0
                    
                    for crypto in SUPPORTED_CRYPTOS:
                        if crypto not in data:
                            data[crypto] = 0.0
                    
                    self.balances = data
            except (json.JSONDecodeError, ValueError):
                self.reset_wallet()
        else:
            self.reset_wallet()

    def reset_wallet(self):
        self.balances = {"USDT": 0.0, **{crypto: 0.0 for crypto in SUPPORTED_CRYPTOS}}
        self.save_wallet()

    def save_wallet(self):
        balances_to_save = {
            key: f"{value:.8f}" if isinstance(value, (int, float)) else value
            for key, value in self.balances.items()
        }
        
        with open(self.filename, "w") as file:
            json.dump(balances_to_save, file, indent=4)
    
    def total_balance(self):
        total_usd = self.balances.get("USDT", 0.0)
        for crypto, amount in self.balances.items():
            if isinstance(amount, (int, float)) and amount > 0:
                if crypto != "USDT":
                    total_usd += float(amount) * CryptoConvert.crypto_rate(crypto)
        print(f"Total balance: {float(total_usd):.2f} USDT")


    def top_up(self, amount):
        self.balances["USDT"] += amount
        self.save_wallet()
        print(f"The balance is replenished by {amount} USDT")
        Transactions.save_transactions(Transactions("top_up", amount, "USDT", "USDT"))

    def usdt_to_crypto(self, crypto, amount):
        if crypto not in SUPPORTED_CRYPTOS:
            print("Error: Unsupported Crypto!")
            return
        if amount > self.balances["USDT"]:
            print("Error: Insufficient funds!")
            return
        rate = CryptoConvert.crypto_rate(crypto)
        crypto_amount = amount / rate
        self.balances["USDT"] -= amount
        self.balances[crypto] += crypto_amount
        self.save_wallet()
        print(f"Converted: {amount} USDT -> {crypto_amount} {crypto}")
        Transactions.save_transactions(Transactions("convert_to_crypto", amount, "USDT", crypto))

    def crypto_to_usdt(self, crypto, amount):
        if crypto not in SUPPORTED_CRYPTOS:
            print("Error: Unsupported Crypto!")
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
        print(f"Converted: {amount} {crypto} -> {usdt_amount} USDT")
        
        Transactions.save_transactions(Transactions("convert_to_usdt", amount, crypto, "USDT"))
