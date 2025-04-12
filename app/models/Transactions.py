import json
from datetime import datetime
import os
from app.utils import clear_console
import uuid
from time import sleep
from app.utils import framed_transaction, framed_menu
from app.interfaces import Color

class Transactions:
    def __init__(self, transactions_type, amount, from_crypto, to_crypto, wallet_address):
        self.transactions_type = transactions_type 
        self.amount = amount
        self.from_crypto = from_crypto
        self.to_crypto = to_crypto
        self.wallet_address = wallet_address
        self.date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.transaction_id = str(uuid.uuid4())

    def to_dict(self):
        return {
            "type": self.transactions_type,
            "amount": self.amount,
            "from": self.from_crypto,
            "to": self.to_crypto,
            "date": self.date,
            "wallet_address": self.wallet_address,
            "id": self.transaction_id
        }


    def save_transactions(transaction):
        filename = "user_transactions.json"
        try:
            with open(filename, "r") as file:
                data = json.load(file)
        except (FileNotFoundError, json.JSONDecodeError):
            data = {"transactions": []}
        data["transactions"].append(transaction.to_dict())
        with open(filename, "w") as file:
            json.dump(data, file, indent=4)

    def view_transactions():
        try:
            filename = "user_transactions.json"
            with open(filename, "r") as file:
                data = json.load(file)
                transactions = data.get("transactions", [])
                    
                if transactions:
                    print("╔════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════╗")
                    print(framed_transaction("Transactions History:"))
                    print("╠════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════╣")
                    for txn in transactions:
                        print(framed_transaction(f"Wallet: {Color.GREEN}{txn['wallet_address']}{Color.RESET} | Date: {Color.YELLOW}{txn['date']}{Color.RESET} | Type: {txn['type']} | From: {Color.BLUE}{txn['from']}{Color.RESET} | To: {Color.BLUE}{txn['to']}{Color.RESET} | Amount: {Color.PURPLE}{txn['amount']:.8f}{Color.RESET}"))
                        print(framed_transaction(" "))
                    print("╚════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════╝")
                choice=input((f"Press 1 to sort transactions or {Color.GRAY}Enter{Color.RESET} to return: "))
                if choice == "1":
                    clear_console()
                    print("")
                    Transactions.sort_transactions(transactions)
                else:
                    print(" ")
        except(FileNotFoundError, json.JSONDecodeError):
            print(f"{Color.RED}No transactions found{Color.RESET}")


    def sort_transactions(transactions):
        while True:
            clear_console()
            print("╔════════════════════════════════════════╗")
            print(framed_menu(f"{Color.BLUE}Choose sorting option{Color.RESET}:"))
            print("╠════════════════════════════════════════╣")
            print(framed_menu(f"{Color.YELLOW}[1]{Color.RESET} Date"))
            print(framed_menu(f"{Color.YELLOW}[2]{Color.RESET} Amount"))
            print(framed_menu(f"{Color.YELLOW}[3]{Color.RESET} Type"))
            print(framed_menu(f"{Color.YELLOW}[4]{Color.RESET} Crypto pairs"))
            print("╚════════════════════════════════════════╝")
            choice = input("Enter option: ")
            
            if choice == "1":
                clear_console()
                while True:
                    order = input(f"Sort by date {Color.GREEN}increase(1){Color.RESET}/{Color.RED}decrease(2){Color.RESET}: ").strip().lower()
                    if order not in ("1", "2"):
                        print(f"{Color.RED}Invalid input. Please enter 1 or 2.{Color.RESET}")
                        continue
                    break

                transactions.sort(key=lambda x: datetime.strptime(x["date"], "%Y-%m-%d %H:%M:%S"), reverse=(order == "2"))

                print("Sorted Transactions History:")
                for txn in transactions:
                    print(f"Wallet: {Color.GREEN}{txn['wallet_address']}{Color.RESET} | Date: {Color.YELLOW}{txn['date']}{Color.RESET} | Type: {txn['type']} | From: {Color.BLUE}{txn['from']}{Color.RESET} | To: {Color.BLUE}{txn['to']}{Color.RESET} | Amount: {Color.PURPLE}{txn['amount']:.8f}{Color.RESET}")
                input(f"Press {Color.GRAY}Enter{Color.RESET} to go back to the menu...")
                break

            elif choice == "2":
                clear_console()
                while True:
                    order = input(f"Sort by amount {Color.GREEN}increase(1){Color.RESET}/{Color.RED}decrease(2){Color.RESET}: ").strip().lower()
                    if order not in ("1", "2"):
                        print(f"{Color.RED}Invalid input. Please enter 1 or 2.{Color.RESET}")
                        continue
                    break

                transactions.sort(key=lambda x: float(x["amount"]), reverse=(order == "2"))

                print("Sorted Transactions History:")
                for txn in transactions:
                    print(f"Wallet: {Color.GREEN}{txn['wallet_address']}{Color.RESET} | Date: {Color.YELLOW}{txn['date']}{Color.RESET} | Type: {txn['type']} | From: {Color.BLUE}{txn['from']}{Color.RESET} | To: {Color.BLUE}{txn['to']}{Color.RESET} | Amount: {Color.PURPLE}{txn['amount']:.8f}{Color.RESET}")
                input(f"Press {Color.GRAY}Enter{Color.RESET} to go back to the menu...")
                break

            elif choice == "3":
                clear_console()
                transaction_types = set(txn["type"].lower() for txn in transactions)
                print("Available transaction types:", ", ".join(transaction_types))
                transaction_type = input("Enter transaction type to filter by: ").strip().lower()
                filtered_transactions = [txn for txn in transactions if txn["type"].lower() == transaction_type]

                if not filtered_transactions:
                    print(f"{Color.RED}No transactions found with this type.{Color.RESET}")
                else:
                    print("Filtered Transactions History:")
                    for txn in filtered_transactions:
                        print(f"Wallet: {Color.GREEN}{txn['wallet_address']}{Color.RESET} | Date: {Color.YELLOW}{txn['date']}{Color.RESET} | Type: {txn['type']} | From: {Color.BLUE}{txn['from']}{Color.RESET} | To: {Color.BLUE}{txn['to']}{Color.RESET} | Amount: {Color.PURPLE}{txn['amount']:.8f}{Color.RESET}")
                
                input(f"Press {Color.GRAY}Enter{Color.RESET} to go back to the menu...")
                break

            elif choice == "4":
                clear_console()
                currencies = set((txn["from"], txn["to"]) for txn in transactions)
                print("Available crypto pairs:", ", ".join([f"{pair[0]} -> {pair[1]}" for pair in currencies]))
                from_currency = input("Enter 'from' crypto: ").strip().upper()
                to_currency = input("Enter 'to' crypto: ").strip().upper()
                filtered_transactions = [txn for txn in transactions if txn["from"] == from_currency and txn["to"] == to_currency]

                if not filtered_transactions:
                    print(f"{Color.RED}No transactions found for this crypto pair.{Color.RESET}")
                else:
                    while True:
                        order = input(f"Sort by currency {Color.GREEN}increase(1){Color.RESET}/{Color.RED}decrease(2){Color.RESET}: ").strip().lower()
                        if order not in ("1", "2"):
                            print(f"{Color.RED}Invalid input. Please enter 1 or 2.{Color.RESET}")
                            continue
                        break

                    filtered_transactions.sort(key=lambda x: (x["from"], x["to"]), reverse=(order == "2"))

                    print("Filtered Transactions History:")
                    for txn in filtered_transactions:
                        print(f"Wallet: {Color.GREEN}{txn['wallet_address']}{Color.RESET} | Date: {Color.YELLOW}{txn['date']}{Color.RESET} | Type: {txn['type']} | From: {Color.BLUE}{txn['from']}{Color.RESET} | To: {Color.BLUE}{txn['to']}{Color.RESET} | Amount: {Color.PURPLE}{txn['amount']:.8f}{Color.RESET}")
                
                input(f"Press {Color.GRAY}Enter{Color.RESET} to go back to the menu...")
                break