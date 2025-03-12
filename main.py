import os
import time
from app.models.CryptoWallet import CryptoWallet
from app.models.Transactions import Transactions

def clear_console():
    os.system("cls" if os.name == "nt" else "clear")

def main():
    wallet = CryptoWallet("user_wallet.json")
    
    while True:
        clear_console()
        wallet.total_balance()
        print("Select an action: ")
        print("1 - Top up your balance in USDT")
        print("2 - Convert USDT to Crypto")
        print("3 - Convert Crypto to USDT")
        print("4 - View transactions")
        print("5 - Exit")
        
        choice = input("Enter action number: ")
        
        if choice == "1":
            clear_console()
            amount = float(input("Enter the amount in USDT: "))
            wallet.top_up(amount)
        elif choice == "2":
            clear_console()
            print(f"Your balance: {wallet.balances['USDT']} USDT")
            crypto = input("Enter Crypto (BTC, ETH, SOL, DOT, TON, DOGE, LTC, XRP, ADA, AVAX): ").upper()
            amount = float(input("Enter the amount in USDT to convert: "))
            wallet.usdt_to_crypto(crypto, amount)
        elif choice == "3":
            clear_console()
            crypto = input("Enter Crypto to convert to USDT (BTC, ETH, SOL, DOT, TON, DOGE, LTC, XRP, ADA, AVAX): ").upper()
            amount = float(input("Enter the amount to convert: "))
            wallet.crypto_to_usdt(crypto, amount)
        elif choice == "4":
            clear_console()
            Transactions.view_transactions()
        elif choice == "5":
            clear_console()
            print("Exit...")
            wallet.save_wallet()
            break
        else:
            print("Invalid input, please try again.")
        
        time.sleep(2)


if __name__ == "__main__":
    main()
