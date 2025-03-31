import os
import json
import uuid
from app.models.CryptoWallet import CryptoWallet
from app.utils import clear_console

class Wallets:
    WALLET_DIR = "wallets"
    
    def __init__(self):
        if not os.path.exists(self.WALLET_DIR):
            os.makedirs(self.WALLET_DIR)
    
    def create_wallet(self):
        clear_console()
        name = input("Enter new wallet name: ")
        address = str(uuid.uuid4())
        wallet_path = os.path.join(self.WALLET_DIR, f"{name}.json")
        wallet = CryptoWallet(wallet_path, address=address)
        wallet.name = name
        wallet.save_wallet()
        print("")
        print(f"Wallet {name} created with address: {address}")
        return wallet
    
    def delete_wallet(self, active_wallet):
        clear_console()
        wallets = self.get_wallets()
        if not wallets:
            print("No available wallets!")
            return
        else:
            for wallet in wallets:
                print(f"{wallet['name']} - {wallet['address']}")
                print("")
        address = input("Enter wallet name to delete: ")
        wallet_path = os.path.join(self.WALLET_DIR, f"{address}.json")

        if os.path.exists(wallet_path):
            os.remove(wallet_path)
            print("Wallet deleted!")

            if active_wallet and active_wallet.address == address:
                active_wallet = None
            return active_wallet

        else:
            print("Wallet not found!")
            return active_wallet

    
    def get_wallets(self):
        wallets = []
        for file in os.listdir(self.WALLET_DIR):
            if file.endswith(".json"):
                wallet_path = os.path.join(self.WALLET_DIR, file)
                with open(wallet_path, "r", encoding="utf-8") as f:
                    data = json.load(f)
                    wallets.append({"name": data.get("name", file[:-5]), "address": data.get("address", "Unknown")})  
        return wallets

    
    def switch_wallet(self, address):
        for file in os.listdir(self.WALLET_DIR):
            wallet_path = os.path.join(self.WALLET_DIR, file)
            if file.endswith(".json"):
                with open(wallet_path, "r", encoding="utf-8") as f:
                    data = json.load(f)
                    if data.get("address") == address:
                        return CryptoWallet(wallet_path, address=address)
        return None
    
    def select_wallet(self):
        clear_console()
        wallets = self.get_wallets()
        if not wallets:
            print("No available wallets!")
            return None
        
        for i, wallet in enumerate(wallets):
            print(f"{i + 1}. {wallet['name']} - {wallet['address']}")
            print("")
        try:
            idx = int(input("Select wallet number: ")) - 1
            active_wallet = self.switch_wallet(wallets[idx]['address'])
            print("")
            print(f"Selected wallet: {wallets[idx]['name']}")
            return active_wallet
        except (IndexError, ValueError):
            print("Invalid selection!")
            return None


    def view_wallets(self):
        clear_console()
        wallets = self.get_wallets()
        if not wallets:
            print("No available wallets!")
        else:
            for wallet in wallets:
                print("")
                print(f"{wallet['name']} - {wallet['address']}")
        input("Press Enter to continue...")

    def transfer_funds(self):
        wallets = self.get_wallets()
        
        if len(wallets) < 2:
            print("Not enough wallets to make a transfer!")
            return
        
        print("Select sender wallet:")
        sender_wallet = self.select_wallet()
        if not sender_wallet:
            return
        
        print("Select receiver wallet:")
        receiver_wallet = self.select_wallet()
        if not receiver_wallet or receiver_wallet.address == sender_wallet.address:
            print("Invalid receiver wallet!")
            return
        
        available_cryptos = {crypto: balance for crypto, balance in sender_wallet.balances.items() if balance > 0}
        
        if not available_cryptos:
            print("Sender has no funds available for transfer!")
            return
        
        print("Available crypto:")
        for i, (crypto, balance) in enumerate(available_cryptos.items(), 1):
            print(f"{i}. {crypto}: {balance}")
        try:
            crypto_choice = int(input("Select crypto number: ")) - 1
            crypto_name = list(available_cryptos.keys())[crypto_choice]
        except (IndexError, ValueError):
            print("Invalid selection!")
            return
        try:
            amount = float(input(f"Enter amount of {crypto_name} to transfer: "))
            if amount <= 0 or amount > available_cryptos[crypto_name]:
                print("Invalid amount!")
                return
        except ValueError:
            print("Invalid input!")
            return
        def withdraw_local(wallet, crypto, amount):
            if wallet.balances[crypto] >= amount:
                wallet.balances[crypto] -= amount
                wallet.save_wallet()
                return True
            else:
                print("Insufficient funds!")
                return False
        def top_up_local(wallet, crypto, amount):
            wallet.balances[crypto] += amount
            wallet.save_wallet()
        
        if withdraw_local(sender_wallet, crypto_name, amount):
            top_up_local(receiver_wallet, crypto_name, amount)
            print(f"Successfully transferred {amount} {crypto_name} from {os.path.basename(sender_wallet.filename)} to {os.path.basename(receiver_wallet.filename)}!")
