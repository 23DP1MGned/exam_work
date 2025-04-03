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
        print(f"The balance is replenished by {Color.BLUE}{amount:.2f} USDT{Color.RESET} from card {Color.GREEN}{formatted_card}{Color.RESET}")
        Transactions.save_transactions(Transactions("Balance replenishment", amount, "my card", "USDT", self.address))
        print("")
        input(f"Press {Color.GRAY}Enter{Color.RESET} to continue...")

    def usdt_to_crypto(self):
        
        print(" ")
        print(f"Your USDT balance: {Color.BLUE}{self.balances.get("USDT", 0)}{Color.RESET} USDT")
        print(" ")
        crypto = input(f"Enter Crypto {Color.PURPLE}(BTC, ETH, SOL, DOT, TON, DOGE, LTC, XRP, ADA, AVAX){Color.RESET} or {Color.GRAY}Enter{Color.RESET} to return: ").upper()
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
        print(f"Converted: {Color.BLUE}{amount:.8f}{Color.RESET} {Color.PURPLE}USDT{Color.RESET} -> {Color.BLUE}{crypto_amount:.8f}{Color.RESET} {Color.PURPLE}{crypto}{Color.RESET}")
        Transactions.save_transactions(Transactions("Converting to crypto", amount, "USDT", crypto, self.address))
        print("")
        input(f"Press {Color.GRAY}Enter{Color.RESET} to continue...")

    def crypto_to_usdt(self):
        filtered_balances = {crypto: amount for crypto, amount in self.balances.items() if amount > 0 and crypto.upper() != "USDT"}

        if not filtered_balances:
            print(f"You have no {Color.PURPLE}Crypto{Color.RESET} on your balance.")
            input(f"Press {Color.GRAY}Enter{Color.RESET} to return...")
            return

        print(f"Your {Color.PURPLE}Crypto{Color.RESET}:")
        print("")
        for crypto, amount in filtered_balances.items():
            print(f"{Color.PURPLE}{crypto}{Color.RESET}: {Color.BLUE}{amount:.8f}{Color.RESET}")
        print(" ")

        crypto = input(f"Enter {Color.PURPLE}Crypto{Color.RESET} to convert or {Color.GRAY}Enter{Color.RESET} to return: ").upper()
        if crypto == "":
            return

        if crypto not in filtered_balances:
            print(f"{Color.RED}Unsupported or empty Crypto!{Color.RESET}")
            return
        try:
            amount = float(input(f"Enter the {Color.BLUE}amount{Color.RESET} to convert: "))
        except ValueError:
            print(f"{Color.RED}Invalid amount!{Color.RESET}")
            return

        if amount > self.balances[crypto]:
            print(f"{Color.RED}Insufficient funds!{Color.RESET}")
            return

        rate = CryptoConvert.crypto_rate(crypto)
        if rate == 0:
            print(f"{Color.RED}Failed to get exchange rate!{Color.RESET}")
            return

        usdt_amount = amount * rate
        self.balances[crypto] -= amount
        self.balances["USDT"] += usdt_amount
        self.save_wallet()

        print(f"Converted: {Color.BLUE}{amount:.8f}{Color.RESET} {Color.PURPLE}{crypto}{Color.RESET} -> {Color.BLUE}{usdt_amount:.8f}{Color.RESET} {Color.PURPLE}USDT{Color.RESET}")

        Transactions.save_transactions(Transactions("Converting to USDT", amount, crypto, "USDT", self.address))

        print(" ")
        input(f"Press {Color.GRAY}Enter{Color.RESET} to continue...")

    def withdraw(self):

        print(f"Available {Color.BLUE}balances{Color.RESET}:")
        print("")
        for crypto, amount in self.balances.items():
            if amount > 0:
                print(f"{Color.PURPLE}{crypto}{Color.RESET}: {Color.BLUE}{amount:.8f}{Color.RESET}")
        print(" ")
        crypto = input(f"Enter the {Color.PURPLE}Crypto{Color.RESET} to withdraw or {Color.GRAY}Enter{Color.RESET} to return: ").upper()
        if crypto == "":
            return
        else:
            amount = float(input(f"Enter the {Color.BLUE}amount{Color.RESET} to withdraw: "))
                
        if crypto not in self.balances:
            print(f"{Color.RED}Unsupported crypto!{Color.RESET}")
            return
        if self.balances[crypto] < amount:
            print(f"{Color.RED}Not enough funds on balance!{Color.RESET}")
            return
        
        card_number = input(f"Enter {Color.GREEN}card number{Color.RESET} (16 digits): ")
        if not (card_number.isdigit() and len(card_number) == 16):
            print(f"{Color.RED}Invalid card data!{Color.RESET}")
            return
        formatted_card = ' '.join([card_number[i:i+4] for i in range(0, 16, 4)])

        
        print("Processing withdraw...")
        time.sleep(random.uniform(2, 4))
        self.balances[crypto] -= amount
        self.save_wallet()
        transaction = Transactions("Withdrawing", amount, crypto, "card number", self.address )
        Transactions.save_transactions(transaction)
        print(f"Withdrawal completed! {Color.BLUE}{amount:.8f}{Color.RESET} {Color.PURPLE}{crypto}{Color.RESET} sent to card {Color.GREEN}{formatted_card}{Color.RESET}.")
        print("")
        input(f"Press {Color.GRAY}Enter{Color.RESET} to continue...")
    
    def view_all_crypto(self):
        print(f"Available {Color.BLUE}balances{Color.RESET}:")
        print("")
        for crypto, amount in self.balances.items():
            if amount > 0:
                print(f"{Color.PURPLE}{crypto}{Color.RESET}: {Color.BLUE}{amount:.8f}{Color.RESET}")
        print(" ")
        input(f"Press {Color.GRAY}Enter{Color.RESET} to continue...")