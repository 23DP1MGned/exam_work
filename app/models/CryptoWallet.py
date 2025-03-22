import json
import os
from app.utils import CryptoConvert
from app.models.Transactions import Transactions
import time
import random

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
                    self.balances["USDT"] = float(data.get("USDT", 0.0))
                    
                    for crypto in SUPPORTED_CRYPTOS:
                        self.balances[crypto] = float(data.get(crypto, 0.0))

            except (json.JSONDecodeError, ValueError):
                self.reset_wallet()
        else:
            self.reset_wallet()


    def reset_wallet(self):
        self.balances = {"USDT": 0.0, **{crypto: 0.0 for crypto in SUPPORTED_CRYPTOS}}
        self.save_wallet()

    def save_wallet(self):
        balances_to_save = {
            key: "{:.8f}".format(float(value)) if isinstance(value, (int, float, str)) else value
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
        print(f" Your total balance: {float(total_usd):.2f} USDT")


    def top_up(self, amount):
        if amount <= 0:
            print("Error: amount must be greater than 0.")
            return
        
        card_number = input("Enter card number (16 digits): ")
        cvc = input("Enter CVC (3 digits):  ")
        date = input("Enter expiration date (MM/YY): ")
            
        if not (card_number.isdigit() and len(card_number) == 16 and cvc.isdigit() and len(cvc) == 3):
            print("Error: Invalid card data.")
            return
            
        print("Processing payment...")
        time.sleep(random.uniform(2, 4))
        self.balances["USDT"] += amount
        self.save_wallet()
        print(f"The balance is replenished by {amount:.2f} USDT")
        Transactions.save_transactions(Transactions("Balance replenishment", amount, "USDT", "USDT"))
        time.sleep(1)

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
        print(f"Converted: {amount:.8f} USDT -> {crypto_amount:.8f} {crypto}")
        Transactions.save_transactions(Transactions("Converting to crypto", amount, "USDT", crypto))

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
        print(f"Converted: {amount:.8f} {crypto} -> {usdt_amount:.8f} USDT")
        
        Transactions.save_transactions(Transactions("Converting to USDT", amount, crypto, "USDT"))

    def withdraw(self, currency, amount):
        if currency not in self.balances:
            print("Error: Unsupported currency.")
            return
        if self.balances[currency] < amount:
            print("Error: Not enough funds on balance.")
            return
        
        card_number = input("Enter card number (16 digits): ")
        if not (card_number.isdigit() and len(card_number) == 16):
            print("Error: Invalid card data.")
            return
        formatted_card = ' '.join([card_number[i:i+4] for i in range(0, 16, 4)])

        
        print("Processing withdraw...")
        time.sleep(random.uniform(2, 4))
        self.balances[currency] -= amount
        self.save_wallet()
        transaction = Transactions("Withdrawing", amount, currency, None)
        Transactions.save_transactions(transaction)
        print(f"Withdrawal completed! {amount:.8f} USDT sent to card {formatted_card}.")
    
    def view_all_crypto(self):
        print("Available balances:")
        print("")
        for currency, amount in self.balances.items():
            if amount > 0:
                print(f"{currency}: {amount:.8f}")
        print(" ")
        input("Press Enter to return to menu...")
