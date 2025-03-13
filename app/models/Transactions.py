import json
from datetime import datetime
import os

class Transactions:
    def __init__(self, transactions_type, amount, from_crypto, to_crypto):
        self.transactions_type = transactions_type 
        self.amount = amount
        self.from_crypto = from_crypto
        self.to_crypto = to_crypto
        self.date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    def to_dict(self):
        return {
            "type": self.transactions_type,
            "amount": self.amount,
            "from": self.from_crypto,
            "to": self.to_crypto,
            "date": self.date
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
                        print(f"Date: {txn['date']} | Type: {txn['type']} | From: {txn['from']} | To: {txn['to']} | Amount: {txn['amount']}")
                        print(" ")
                print("Press 1 to sort transactions or Enter to go to menu")
                choice = input("Enter option: ")
                if choice == "1":
                    print("")
                    Transactions.sort_transactions(transactions)
                else:
                    print(" ")
           # input("Press Enter to go back to the menu...")
        except(FileNotFoundError, json.JSONDecodeError):
            print("No transactions found")

    def sort_transactions(transactions):
        print("Choose sorting option:")
        print("1 - Date")
        print("2 - Amount")
        print("3 - Type")
        print("4 - From-To Currency")
        choice = input("Enter option (1-4): ")
        
        if choice == "1":
            transactions.sort(key=lambda x: datetime.strptime(x["date"], "%Y-%m-%d %H:%M:%S"), reverse=True)
        elif choice == "2":
            transactions.sort(key=lambda x: float(x["amount"]), reverse=True)
        elif choice == "3":
            transactions.sort(key=lambda x: x["type"].lower())
        elif choice == "4":
            transactions.sort(key=lambda x: (x["from"], x["to"]))
        
        print("Sorted Transactions History:")
        for txn in transactions:
            print(f"Date: {txn['date']} | Type: {txn['type']} | From: {txn['from']} | To: {txn['to']} | Amount: {txn['amount']}")
            print(" ")
        input("Press Enter to go back to the menu...")