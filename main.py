import os
import json
import time
from app.models.CryptoWallet import CryptoWallet
from app.utils import CryptoConvert

def clear_console():
    os.system("cls" if os.name == "nt" else "clear")

def main():
    wallet = CryptoWallet("user_wallet.json")
    
    while True:
        clear_console()
        print("Current balance:")
        wallet.total_balance()
        print("Select an action: ")
        print("1 - Top up your balance in USDT")
        print("2 - Convert USDT to Cryptocurrency")
        print("3 - Convert cryptocurrency back to USDT")
        print("4 - Exit")
        
        choice = input("Enter action number: ")
        
        if choice == "1":
            amount = float(input("Enter the amount in USDT:"))
            wallet.top_up(amount)
        elif choice == "2":
            crypto = input("Enter cryptocurrency (BTC, ETH, SOL, DOT, TON, DOGE, LTC, XRP, ADA, AVAX): ").upper()
            amount = float(input("Enter the amount in USDT to convert:"))
            wallet.usdt_to_crypto(crypto, amount)
        elif choice == "3":
            crypto = input("Enter cryptocurrency to convert to USDT:").upper()
            amount = float(input("Enter the amount to convert:"))
            wallet.crypto_to_usdt(crypto, amount)
        elif choice == "4":
            print("Exit...")
            wallet.save_wallet()
            break
        else:
            print("Invalid input, please try again.")
        
        time.sleep(2)

if __name__ == "__main__":
    main()
