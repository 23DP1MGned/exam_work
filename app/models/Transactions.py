import json
from datetime import datetime

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

    @staticmethod
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
