import json
from datetime import datetime
from app.utils import CryptoConvert


class CryptoWallet:
    def __init__(self, user):
        self.user = user
        self.balance_eur = 0.0
        self.balance_btc = 0.0
        self.transactions = []

    def top_up(self, amount_eur):
        self.balance_eur += amount_eur
        self.transactions.append({
            "type": "top_up",
            "amount_eur": amount_eur,
            "date": str(datetime.now())
        })
        print(f"Balance replenished: {amount_eur} EUR")
        self.show_balance()

    def convert_to_btc(self, amount_eur):
        if amount_eur > self.balance_eur:
            print("Error: Not enough funds in EUR!")
            return
        rate = CryptoConvert.get_btc_exchange_rate("eur")
        btc_received = amount_eur / rate
        self.balance_eur -= amount_eur
        self.balance_btc += btc_received
        self.transactions.append({
            "type": "conversion",
            "amount_eur": amount_eur,
            "amount_btc": btc_received,
            "date": str(datetime.now())
        })
        print(f"Conversion complete: {amount_eur} EUR -> {btc_received:.8f} BTC")
        self.show_balance()

    def show_balance(self):
        print(f"Current balance: {self.balance_eur:.2f} EUR | {self.balance_btc:.8f} BTC")

    def save_to_file(self):
        with open(f"{self.user}_wallet.json", "w") as f:
            json.dump({
                "balance_eur": self.balance_eur,
                "balance_btc": self.balance_btc,
                "transactions": self.transactions
            }, f, indent=4)
