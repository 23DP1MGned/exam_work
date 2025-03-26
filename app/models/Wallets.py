import os
import json
import uuid
from app.models.CryptoWallet import CryptoWallet

class Wallets:
    WALLET_DIR = "wallets"
    
    def __init__(self):
        if not os.path.exists(self.WALLET_DIR):
            os.makedirs(self.WALLET_DIR)
    
    def create_wallet(self, name):
        wallet_address = str(uuid.uuid4())
        wallet_path = os.path.join(self.WALLET_DIR, f"{name}.json")
        wallet = CryptoWallet(wallet_path, address=wallet_address)
        wallet.name = name
        wallet.save_wallet()
        
        return wallet_address
    
    def delete_wallet(self, wallet_address):
        wallet_path = os.path.join(self.WALLET_DIR, f"{wallet_address}.json")
        if os.path.exists(wallet_path):
            os.remove(wallet_path)
            return True
        return False
    
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
    
