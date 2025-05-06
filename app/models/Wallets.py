import os
import json
import uuid
from app.models.CryptoWallet import CryptoWallet
from app.utils import clear_console, framed_adress
from app.interfaces import Color
import time

class Wallets:
    WALLET_DIR = "wallets"
    
    def __init__(self):
        if not os.path.exists(self.WALLET_DIR):
            os.makedirs(self.WALLET_DIR)
    
    def create_wallet(self):
        clear_console()
        print(f"Creating a new {Color.BLUE}wallet{Color.RESET}:")
        print(" ")
        while True:
            name = input(f"Enter new {Color.BLUE}wallet name{Color.RESET} or press {Color.GRAY}Enter{Color.RESET} to return: ")
            if name == "":
                return
            wallet_path = os.path.join(self.WALLET_DIR, f"{name}.json")
        
            if os.path.exists(wallet_path):
                print(f"{Color.RED}A wallet with the name {Color.BLUE}{name}{Color.RED} already exists.{Color.RESET} {Color.GREEN}Please choose a different name.{Color.RESET}")
                print("")
            else:
                break
        
        address = str(uuid.uuid4())
        wallet = CryptoWallet(wallet_path, address=address)
        wallet.name = name
        wallet.save_wallet()
        print("")
        print(f"Wallet {Color.BLUE}{name}{Color.RESET} created with address: {Color.GREEN}{address}{Color.RESET}")
        print("")
        input(f"Press {Color.GRAY}Enter{Color.RESET} to continue...")
        return wallet
    
    def delete_wallet(self, active_wallet):
        wallets = self.get_wallets()
        if not wallets:
            print(f"{Color.RED}No available wallets!{Color.RESET}")
            return
        else:
            clear_console()
            print("╔═════════════════════════════════════════════════════════════════════╗")
            print(framed_adress(f"Your {Color.BLUE}wallets{Color.RESET}:"))
            print("╠═════════════════════════════════════════════════════════════════════╣")
            for i ,wallet in enumerate(wallets):
                print(framed_adress(f"{Color.BLUE}{wallet['name']}{Color.RESET} - {Color.GREEN}{wallet['address']}{Color.RESET}"))
                if i != len(wallets) - 1:
                    print(framed_adress(""))
            print("╚═════════════════════════════════════════════════════════════════════╝")
        address = input(f"Enter {Color.BLUE}wallet name{Color.RESET} to delete or Press {Color.GRAY}Enter{Color.RESET} to return: ")
        if address == "":
            return
        wallet_path = os.path.join(self.WALLET_DIR, f"{address}.json")

        if os.path.exists(wallet_path):
            os.remove(wallet_path)
            print(f"{Color.RED}Wallet deleted!{Color.RESET}")
            time.sleep(1.5)

            if active_wallet and active_wallet.address == address:
                active_wallet = None
            return active_wallet

        else:
            print(f"{Color.RED}Wallet not found!{Color.RESET}")
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
        wallets = self.get_wallets()
        if not wallets:
            print(f"{Color.RED}No available wallets{Color.RESET}, please create a new {Color.BLUE}wallet{Color.RESET}")
            return None
        clear_console()
        print("╔═════════════════════════════════════════════════════════════════════╗")
        print(framed_adress(f"Your {Color.BLUE}wallets{Color.RESET}:"))
        print("╠═════════════════════════════════════════════════════════════════════╣")
        for i, wallet in enumerate(wallets):
            print(framed_adress(f"{i + 1}. {Color.BLUE}{wallet['name']}{Color.RESET} - {Color.GREEN}{wallet['address']}{Color.RESET}"))
            if i != len(wallets) - 1:
                print(framed_adress(""))
        print("╚═════════════════════════════════════════════════════════════════════╝")
        try:
            idx = input(f"Select {Color.BLUE}wallet{Color.RESET} number or press {Color.GRAY}Enter{Color.RESET} to return: ")
            if idx == "":
                return
            else:
                idx = int(idx)-1
            active_wallet = self.switch_wallet(wallets[idx]['address'])
            print(f"Selected wallet: {Color.BLUE}{wallets[idx]['name']}{Color.RESET}")
            #time.sleep(1)
            return active_wallet
        except (IndexError, ValueError):
            print(f"{Color.RED}Invalid selection!{Color.RESET}")
            return None


    def view_wallets(self):
        clear_console()
        wallets = self.get_wallets()
        if not wallets:
            print(f"{Color.RED}No available wallets{Color.RESET}!")
        else:
            print("╔═════════════════════════════════════════════════════════════════════╗")
            print(framed_adress(f"Available {Color.BLUE}wallets{Color.RESET}:"))
            print("╠═════════════════════════════════════════════════════════════════════╣")
            for i ,wallet in enumerate(wallets):
                print(framed_adress(f"{Color.BLUE}{wallet['name']}{Color.RESET} - {Color.GREEN}{wallet['address']}{Color.RESET}"))
                if i != len(wallets) - 1:
                    print("╠═════════════════════════════════════════════════════════════════════╣")
            print("╚═════════════════════════════════════════════════════════════════════╝")
        input(f"Press {Color.GRAY}Enter{Color.RESET} to continue...")

    def transfer_funds(self, active_wallet):
        wallets = self.get_wallets()
        
        if len(wallets) < 2:
            print(f"{Color.RED}Not enough wallets to make a transfer!{Color.RESET}")
            return
        clear_console()
        print("╔═════════════════════════════════════════════════════════════════════╗")
        print(framed_adress(f"Available {Color.BLUE}wallets{Color.RESET}:"))
        print("╠═════════════════════════════════════════════════════════════════════╣")
        for i, wallet in enumerate(wallets):
            print(framed_adress(f"{i + 1}. {Color.BLUE}{wallet['name']}{Color.RESET} - {Color.GREEN}{wallet['address']}{Color.RESET}"))
            if i != len(wallets) - 1:
                print(framed_adress(""))
        print("╚═════════════════════════════════════════════════════════════════════╝")
        try:
            print("")
            sender_index = input(f"Select sender {Color.BLUE}wallet{Color.RESET} number or press {Color.GRAY}Enter{Color.RESET} to return: ")
            if sender_index == "":
                return
            else:
                sender_index = int(sender_index)-1
            sender_wallet_data = wallets[sender_index]
        except (IndexError, ValueError):
            print(f"{Color.RED}Invalid selection!{Color.RESET}")
            return
        
        sender_wallet = self.switch_wallet(sender_wallet_data['address'])
        try:
            receiver_index = int(input(f"Select receiver {Color.BLUE}wallet{Color.RESET} number: ")) - 1
            if receiver_index == sender_index:
                print(f"{Color.RED}You cannot send funds to the same wallet!{Color.RESET}")
                return
            receiver_wallet_data = wallets[receiver_index]
        except (IndexError, ValueError):
            print(f"{Color.RED}Invalid selection!{Color.RESET}")
            return
        
        receiver_wallet = self.switch_wallet(receiver_wallet_data['address'])
        available_cryptos = {crypto: balance for crypto, balance in sender_wallet.balances.items() if balance > 0}
        
        if not available_cryptos:
            print(f"{Color.RED}Sender has no funds available for transfer!{Color.RESET}")
            return
        
        print("")
        print(f"Available {Color.PURPLE}crypto{Color.RESET} of the sender's wallet:")
        crypto_list = list(available_cryptos.keys())
        for i, crypto in enumerate(crypto_list, 1):
            print(f"{i}. {Color.PURPLE}{crypto}{Color.RESET}: {available_cryptos[crypto]}")

        try:
            crypto_choice = int(input(f"\nSelect {Color.PURPLE}crypto{Color.RESET} number: ")) - 1
            crypto_name = crypto_list[crypto_choice]
        except (IndexError, ValueError):
            print(f"{Color.RED}Invalid selection!{Color.RESET}")
            return

        try:
            amount = float(input(f"Enter amount of {Color.PURPLE}{crypto_name}{Color.RESET} to transfer: "))
            if amount <= 0 or amount > available_cryptos[crypto_name]:
                print(f"{Color.RED}Invalid amount!{Color.RESET}")
                return
        except ValueError:
            print(f"{Color.RED}Invalid input!{Color.RESET}")
            return
        
        
        def withdraw_local(wallet, crypto, amount):
            if wallet.balances[crypto] >= amount:
                wallet.balances[crypto] -= amount
                wallet.save_wallet()
                return True
            else:
                print(f"{Color.RED}Insufficient funds!{Color.RESET}")
                return False
        def top_up_local(wallet, crypto, amount):
            wallet.balances[crypto] += amount
            wallet.save_wallet()
        
        if withdraw_local(sender_wallet, crypto_name, amount):
            top_up_local(receiver_wallet, crypto_name, amount)
            if active_wallet and (sender_wallet.address == active_wallet.address or receiver_wallet.address == active_wallet.address):
                active_wallet = self.switch_wallet(active_wallet.address)
            print(f"Successfully transferred {Color.BLUE}{amount}{Color.RESET} {Color.PURPLE}{crypto_name}{Color.RESET} from {Color.GREEN}{os.path.splitext(os.path.basename(sender_wallet.filename))[0]}{Color.RESET} to {Color.GREEN}{os.path.splitext(os.path.basename(receiver_wallet.filename))[0]}{Color.RESET}!")
            print("")
            input(f"Press {Color.GRAY}Enter{Color.RESET} to continue...")
            return active_wallet
