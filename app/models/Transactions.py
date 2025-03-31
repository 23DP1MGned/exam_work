import json
from datetime import datetime
import os
from app.utils import clear_console
import uuid
from time import sleep

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
                    print("Transactions History:")
                    print(" ")
                    for txn in transactions:
                        print(f"Wallet: {txn['wallet_address']} | Date: {txn['date']} | Type: {txn['type']} | From: {txn['from']} | To: {txn['to']} | Amount: {txn['amount']}")
                        print(" ")
                choice=input(("Press 1 to sort transactions or Enter to go to menu: "))
                if choice == "1":
                    clear_console()
                    print("")
                    Transactions.sort_transactions(transactions)
                else:
                    print(" ")
           # input("Press Enter to go back to the menu...")
        except(FileNotFoundError, json.JSONDecodeError):
            print("No transactions found")


    def sort_transactions(transactions):
        while True:
            clear_console()
            print("Choose sorting option:")
            print("1 - Date")
            print("2 - Amount")
            print("3 - Type")
            print("4 - Crypto pairs")
            choice = input("Enter option (1-4): ")
            
            if choice == "1":
                clear_console()
                order = input("Sort by date increase(1)/decrease(2): ").strip().lower()
                transactions.sort(key=lambda x: datetime.strptime(x["date"], "%Y-%m-%d %H:%M:%S"), reverse=(order == "2"))

                print("Sorted Transactions History:")
                print("")
                for txn in transactions:
                    print(f"Wallet: {txn['wallet_address']} | Date: {txn['date']} | Type: {txn['type']} | From: {txn['from']} | To: {txn['to']} | Amount: {txn['amount']}")
                input("Press Enter to go back to the menu...")
                break


            elif choice == "2":
                clear_console()
                order = input("Sort by amount increase(1)/decrease(2): ").strip().lower()
                transactions.sort(key=lambda x: float(x["amount"]), reverse=(order == "2"))

                print("Sorted Transactions History:")
                print("")
                for txn in transactions:
                    print(f"Wallet: {txn['wallet_address']} | Date: {txn['date']} | Type: {txn['type']} | From: {txn['from']} | To: {txn['to']} | Amount: {txn['amount']}")
                input("Press Enter to go back to the menu...")
                break


            elif choice == "3":
                clear_console()
                transaction_types = set(txn["type"].lower() for txn in transactions)
                print("Available transaction types:", ", ".join(transaction_types))
                transaction_type = input("Enter transaction type to filter by: ").strip().lower()
                transactions = [txn for txn in transactions if txn["type"].lower() == transaction_type]

                print("Sorted Transactions History:")
                print("")
                for txn in transactions:
                    print(f"Wallet: {txn['wallet_address']} | Date: {txn['date']} | Type: {txn['type']} | From: {txn['from']} | To: {txn['to']} | Amount: {txn['amount']}")
                input("Press Enter to go back to the menu...")
                break


            elif choice == "4":
                clear_console()
                currencies = set((txn["from"], txn["to"]) for txn in transactions)
                print("Available crypto pairs:", ", ".join([f"{pair[0]} -> {pair[1]}" for pair in currencies]))
                from_currency = input("Enter 'from' crypto: ").strip().upper()
                to_currency = input("Enter 'to' crypto: ").strip().upper()
                transactions = [txn for txn in transactions if txn["from"] == from_currency and txn["to"] == to_currency]
                order = input("Sort by currency increase(1)/decrease(2): ").s0trip().lower()
                transactions.sort(key=lambda x: (x["from"], x["to"]), reverse=(order == "2"))

                print("Sorted Transactions History:")
                print("")
                for txn in transactions:
                    print(f"Wallet: {txn['wallet_address']} | Date: {txn['date']} | Type: {txn['type']} | From: {txn['from']} | To: {txn['to']} | Amount: {txn['amount']}")
                input("Press Enter to go back to the menu...")
                break


            else:
                print(" ")
                print("Invalid input, please try again.")
                sleep(2)
            
