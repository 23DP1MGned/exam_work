import os
import time
from app.models.CryptoWallet import CryptoWallet
from app.models.Transactions import Transactions
from app.models.Wallets import Wallets
from app.utils import clear_console

def main():
    multi_wallet = Wallets()
    active_wallet = None
    
    while True:
        clear_console()
        print(" ")
        print("___________________________________")
        print("|         Select an action:         |")
        print("|                                   | ")
        print("|  1 - Select wallet                |")
        print("|  2 - Create new wallet            |")
        print("|  3 - Delete wallet                |")
        print("|  4 - View all wallets             |")
        print("|  5 - Wallet operations            |")
        print("|  6 - Exit                         |")
        print("___________________________________")
        print(" ")
        
        choice = input("Enter action number: ")
        
        if choice == "1":
            wallets = multi_wallet.get_wallets()
            if not wallets:
                print("No available wallets!")
            else:
                for i, wallet in enumerate(wallets):
                    print(f"{i + 1}. {wallet['name']} - {wallet['address']}")
                try:
                    idx = int(input("Select wallet number: ")) - 1
                    active_wallet = multi_wallet.switch_wallet(wallets[idx]['address'])
                    print(f"Selected wallet: {wallets[idx]['name']}")
                except (IndexError, ValueError):
                    print("Invalid selection!")
            time.sleep(2)
        
        elif choice == "2":
            name = input("Enter new wallet name: ")
            wallet_address = multi_wallet.create_wallet(name)
            print(f"Wallet {name} created with address {wallet_address}")
            time.sleep(2)
        
        elif choice == "3":
            wallet_address = input("Enter wallet address to delete: ")
            if multi_wallet.delete_wallet(wallet_address):
                print("Wallet deleted!")
                if active_wallet and active_wallet.wallet_address == wallet_address:
                    active_wallet = None
            else:
                print("Wallet not found!")
            time.sleep(2)
        
        elif choice == "4":
            wallets = multi_wallet.get_wallets()
            if not wallets:
                print("No available wallets!")
            else:
                for wallet in wallets:
                    print(f"{wallet['name']} - {wallet['address']}")
            input("Press Enter to continue...")
        
        elif choice == "5":
            if not active_wallet:
                print("No active wallet selected!")
                time.sleep(2)
                continue
            while True:
                clear_console()
                active_wallet.total_balance()
                print("___________________________________")
                print("|        Select an action:       |")
                print("|                                | ")
                print("|  1 - Top up balance in USDT    |")
                print("|  2 - Convert USDT to Crypto    |")
                print("|  3 - Convert Crypto to USDT    |")
                print("|  4 - View transactions         |")
                print("|  5 - Withdraw funds            |")
                print("|  6 - View your crypto          |")
                print("|  7 - Back                      |")
                print("___________________________________")
                print(" ")
                
                sub_choice = input("Enter action number: ")
                
                if sub_choice == "1":
                    clear_console()
                    active_wallet.top_up()
                elif sub_choice == "2":
                    clear_console()
                    active_wallet.usdt_to_crypto()
                elif sub_choice == "3":
                    clear_console()
                    active_wallet.crypto_to_usdt()
                elif sub_choice == "4":
                    clear_console()
                    Transactions.view_transactions()
                elif sub_choice == "5":
                    clear_console()
                    active_wallet.withdraw()
                elif sub_choice == "6":
                    clear_console()
                    active_wallet.view_all_crypto()
                elif sub_choice == "7":
                    break
                else:
                    print("Invalid input, please try again.")
                time.sleep(1)
        
        elif choice == "6":
            clear_console()
            print("Exit...")
            if active_wallet:
                active_wallet.save_wallet()
            break
        else:
            print("Invalid input, please try again.")
        
        time.sleep(1)

if __name__ == "__main__":
    main()
