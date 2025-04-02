import json
import os
from app.utils import CryptoConvert, Color
from app.models.Transactions import Transactions
import time
import random

SUPPORTED_CRYPTOS = ["BTC", "ETH", "SOL", "DOT", "TON", "DOGE", "LTC", "XRP", "ADA", "AVAX"]

class CryptoWallet:
    def __init__(self, filename, address=None):
        self.filename = filename
        self.address = address
        self.balances = {"USDT": 0.0, **{crypto: 0.0 for crypto in SUPPORTED_CRYPTOS}}
        self.load_wallet()
    
    def load_wallet(self):
        if os.path.exists(self.filename):
            try:
                with open(self.filename, "r") as file:
                    data = json.load(file)

                    if "USDT" not in data:
                        data["USDT"] = 0.0
                    self.address = data.get("address", self.address)
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
            "address": self.address,
            **{
                key: "{:.8f}".format(float(value)) if isinstance(value, (int, float, str)) else value
                for key, value in self.balances.items()
            }
        }
        
        with open(self.filename, "w") as file:
            json.dump(balances_to_save, file, indent=4)

    
    def total_balance(self):
        total_usd = self.balances.get("USDT", 0.0)
        for crypto, amount in self.balances.items():
            if isinstance(amount, (int, float)) and amount > 0:
                if crypto != "USDT":
                    total_usd += float(amount) * CryptoConvert.crypto_rate(crypto)
        print(f" Your total balance: {Color.BLUE}{float(total_usd):.2f} USDT{Color.RESET}")


    def top_up(self):
        amount = input(f"Enter the amount in {Color.BLUE}USDT{Color.RESET} or {Color.GRAY}Enter{Color.RESET} to return: ")
        if amount == "":
            return
        else:
            amount = float(amount)
        if amount <= 0:
            print(f"{Color.RED}Amount must be greater than 0.{Color.RESET}")
            return
        
        card_number = input(f"Enter {Color.GREEN}card number{Color.RESET} (16 digits): ")
        cvc = input(f"Enter {Color.GREEN}CVC{Color.RESET} (3 digits):  ")
        date = input(f"Enter {Color.GREEN}expiration date{Color.RESET} (MM/YY): ")
        formatted_card = ' '.join([card_number[i:i+4] for i in range(0, 16, 4)])
            
        if not (card_number.isdigit() and len(card_number) == 16 and cvc.isdigit() and len(cvc) == 3):
            print(f"{Color.RED}Error: Invalid card data.{Color.RESET}")
            return
            
        print("Processing payment...")
        time.sleep(random.uniform(2, 4))
        self.balances["USDT"] += amount
        self.save_wallet()
        print(f"The balance is replenished by {Color.BLUE}{amount:.2f}{Color.BLUE} USDT from card {Color.GREEN}{formatted_card}{Color.GREEN}")
        Transactions.save_transactions(Transactions("Balance replenishment", amount, "USDT", "USDT", self.address))
        time.sleep(1)

    def usdt_to_crypto(self):
        
        print(" ")
        print(f"Your USDT balance: {Color.BLUE}{self.balances.get("USDT", 0)}{Color.RESET} USDT")
        print(" ")
        crypto = input("Enter Crypto (BTC, ETH, SOL, DOT, TON, DOGE, LTC, XRP, ADA, AVAX) or Enter to return: ").upper()
        if crypto == "":
            return
        else:
            amount = float(input(f"Enter the amount in {Color.BLUE}USDT{Color.RESET} to convert: "))
        if crypto not in SUPPORTED_CRYPTOS:
            print(f"{Color.RED}Unsupported Crypto!{Color.RESET}")
            return
        if amount > self.balances["USDT"]:
            print(f"{Color.RED}Insufficient funds!{Color.RESET}")
            return
        rate = CryptoConvert.crypto_rate(crypto)
        crypto_amount = amount / rate
        self.balances["USDT"] -= amount
        self.balances[crypto] += crypto_amount
        self.save_wallet()
        print(f"Converted: {Color.BLUE}{amount:.8f}{Color.RESET} USDT -> {Color.PURPLE}{crypto_amount:.8f}{Color.RESET} {Color.BLUE}{crypto}{Color.RESET}")
        Transactions.save_transactions(Transactions("Converting to crypto", amount, "USDT", crypto, self.address))

    def crypto_to_usdt(self):

        filtered_balances = {crypto: amount for crypto, amount in self.balances.items() if amount > 0 and crypto.upper() != "USDT"}
        if filtered_balances:
            print("Your Crypto:")
            print(" ")
            for crypto, amount in filtered_balances.items():
                print(f"{crypto}: {Color.PURPLE}{amount:.8f}{Color.RESET}")
        else:
            print("You have no Сrypto on your balance.")
        if filtered_balances:
            print(" ")
            crypto = input("Enter Crypto or Enter to return: ").upper()
            if crypto == "":
                    return
            else:
                amount = float(input("Enter the amount to convert: "))
        else:
            print(" ")
            input("Press Enter to return to the main menu...")

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
        
        Transactions.save_transactions(Transactions("Converting to USDT", amount, crypto, "USDT", self.address))

    def withdraw(self):

        print("Available balances:")
        print("")
        for crypto, amount in self.balances.items():
            if amount > 0:
                print(f"{crypto}: {amount:.8f}")
        print(" ")
        crypto = input("Enter the crypto to withdraw or Enter to return: ").upper()
        if crypto == "":
            return
        else:
            amount = float(input("Enter the amount to withdraw: "))
            time.sleep(2)
                
        if crypto not in self.balances:
            print("Error: Unsupported crypto.")
            return
        if self.balances[crypto] < amount:
            print("Error: Not enough funds on balance.")
            return
        
        card_number = input("Enter card number (16 digits): ")
        if not (card_number.isdigit() and len(card_number) == 16):
            print("Error: Invalid card data.")
            return
        formatted_card = ' '.join([card_number[i:i+4] for i in range(0, 16, 4)])

        
        print("Processing withdraw...")
        time.sleep(random.uniform(2, 4))
        self.balances[crypto] -= amount
        self.save_wallet()
        transaction = Transactions("Withdrawing", amount, crypto, None, self.address )
        Transactions.save_transactions(transaction)
        print(f"Withdrawal completed! {amount:.8f} {crypto} sent to card {formatted_card}.")
        time.sleep(2)
    
    def view_all_crypto(self):
        print("Available balances:")
        print("")
        for crypto, amount in self.balances.items():
            if amount > 0:
                print(f"{crypto}: {amount:.8f}")
        print(" ")
        input("Press Enter to return to menu...")