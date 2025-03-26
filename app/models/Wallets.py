import os
import json
import uuid
from app.models.CryptoWallet import CryptoWallet

class Wallets:
    WALLET_DIR = "wallets"
    
    def __init__(self):
        if not os.path.exists(self.WALLET_DIR):
            os.makedirs(self.WALLET_DIR)
    
    def create_wallet(self):
        name = input("Enter new wallet name: ")
        wallet_address = str(uuid.uuid4())
        wallet_path = os.path.join(self.WALLET_DIR, f"{name}.json")
        wallet = CryptoWallet(wallet_path, address=wallet_address)
        wallet.name = name
        wallet.save_wallet()
        
        print(f"Wallet {name} created with address {wallet_address}")
        return wallet
    
    def delete_wallet(self, active_wallet):
        wallets = self.get_wallets()
        if not wallets:
            print("No available wallets!")
            return
        else:
            for wallet in wallets:
                print(f"{wallet['name']} - {wallet['address']}")
        wallet_address = input("Enter wallet name to delete: ")
        wallet_path = os.path.join(self.WALLET_DIR, f"{wallet_address}.json")

        if os.path.exists(wallet_path):
            os.remove(wallet_path)
            print("Wallet deleted!")

            if active_wallet and active_wallet.wallet_address == wallet_address:
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

    
    def switch_wallet(self, wallet_address):
        for file in os.listdir(self.WALLET_DIR):
            wallet_path = os.path.join(self.WALLET_DIR, file)
            if file.endswith(".json"):
                with open(wallet_path, "r", encoding="utf-8") as f:
                    data = json.load(f)
                    if data.get("address") == wallet_address:
                        return CryptoWallet(wallet_path, address=wallet_address)
        return None
    
    def select_wallet(self):
        wallets = self.get_wallets()
        if not wallets:
            print("No available wallets!")
            return None

        for i, wallet in enumerate(wallets):
            print(f"{i + 1}. {wallet['name']} - {wallet['address']}")

        try:
            idx = int(input("Select wallet number: ")) - 1
            active_wallet = self.switch_wallet(wallets[idx]['address'])
            print(f"Selected wallet: {wallets[idx]['name']}")
            return active_wallet
        except (IndexError, ValueError):
            print("Invalid selection!")
            return None


    def view_wallets(self):
        wallets = self.get_wallets()
        if not wallets:
            print("No available wallets!")
        else:
            for wallet in wallets:
                print(f"{wallet['name']} - {wallet['address']}")
        input("Press Enter to continue...")

