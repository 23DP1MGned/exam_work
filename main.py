import os
import time
from app.models.CryptoWallet import CryptoWallet
from app.models.Transactions import Transactions
from app.utils import clear_console

def main():
    wallet = CryptoWallet("user_wallet.json")
    
    while True:
        clear_console()
        print(" ")
        wallet.total_balance()
        print("___________________________________")
        print("|         Select an action:         |")
        print("|                                   | ")
        print("|  1 - Top up your balance in USDT  |")
        print("|  2 - Convert USDT to Crypto       |")
        print("|  3 - Convert Crypto to USDT       |")
        print("|  4 - View transactions            |")
        print("|  5-  Withdraw funds               |")
        print("|  6-  View your crypto             |")
        print("|  7 - Exit                         |")
        print("___________________________________")
        print(" ")
        
        choice = input("Enter action number: ")
        
        if choice == "1":
            clear_console()
            wallet.top_up()
        elif choice == "2":
            clear_console()
            wallet.usdt_to_crypto()
        elif choice == "3":
            clear_console()
            wallet.crypto_to_usdt()
        elif choice == "4":
            clear_console()
            Transactions.view_transactions()
        elif choice == "5":
            clear_console()
            wallet.withdraw()
        elif choice == "6":
            clear_console()
            wallet.view_all_crypto()
        elif choice == "7":
            clear_console()
            print("Exit...")
            wallet.save_wallet()
            break
        else:
            print("Invalid input, please try again.")
        
        time.sleep(1)


if __name__ == "__main__":
    main()
