import time
import os
from app.models.CryptoWallet import CryptoWallet
from app.models.Transactions import Transactions
from app.models.Wallets import Wallets
from app.utils import clear_console, framed_menu
from app.interfaces import asci_wallet, Color
from app.models.User import User

def app_main():
    multi_wallet = Wallets()
    active_wallet = None
    User.authenticate()
    
    while True:
        clear_console()
        print(" ")
        print("╔════════════════════════════════════════╗")
        print("║             Wallet Menu                ║")
        print("╠════════════════════════════════════════╣")
        if active_wallet:
            print(framed_menu(f"Selected Wallet: {Color.BLUE}{os.path.splitext(os.path.basename(active_wallet.filename))[0]}{Color.RESET}"))
        else:
            print(framed_menu(f"No {Color.BLUE}Wallet{Color.RESET} selected! "))
        print("╠════════════════════════════════════════╣")
        print(f"║  {Color.YELLOW}[1]{Color.RESET} Select wallet                     ║")
        print(f"║  {Color.YELLOW}[2]{Color.RESET} Create new wallet                 ║")
        print(f"║  {Color.YELLOW}[3]{Color.RESET} Delete wallet                     ║")
        print(f"║  {Color.YELLOW}[4]{Color.RESET} View all wallets                  ║")
        print(f"║  {Color.YELLOW}[5]{Color.RESET} Transfer funds                    ║")
        print(f"║  {Color.YELLOW}[6]{Color.RESET} View transactions                 ║")
        print(f"║  {Color.YELLOW}[7]{Color.RESET} Wallet operations                 ║")
        print(f"║  {Color.YELLOW}[8]{Color.RESET} {Color.RED}Exit{Color.RESET}                              ║")
        print("╚════════════════════════════════════════╝")
        print(" ")
        
        choice = input("Enter action number: ")
        
        if choice == "1":
            active_wallet = multi_wallet.select_wallet()
            time.sleep(1)
        
        elif choice == "2":
            multi_wallet.create_wallet()
            time.sleep(1)
        
        elif choice == "3":
            multi_wallet.delete_wallet(active_wallet)   
            time.sleep(1)
        
        elif choice == "4":
            multi_wallet.view_wallets()
            time.sleep(1)

        elif choice == "5":
            new_wallet = multi_wallet.transfer_funds(active_wallet)
            if new_wallet is not None:
                active_wallet = new_wallet
            time.sleep(1)

        elif choice == "6":
            clear_console()
            Transactions.view_transactions()

        elif choice == "7":
            if not active_wallet:
                print(f"{Color.RED}No active wallet selected{Color.RESET}, please select {Color.BLUE}wallet{Color.RESET}!")
                time.sleep(2.5)
                continue
            while True:
                clear_console()
                print(" ")
                active_wallet.total_balance()

                print("╔═══════════════════════════════════════╗")
                print("║           Wallet Operations           ║")
                print("╠═══════════════════════════════════════╣")
                print(f"║  {Color.YELLOW}[1]{Color.RESET} Top up balance in USDT           ║")
                print(f"║  {Color.YELLOW}[2]{Color.RESET} Convert USDT to Crypto           ║")
                print(f"║  {Color.YELLOW}[3]{Color.RESET} Convert Crypto to USDT           ║")
                print(f"║  {Color.YELLOW}[4]{Color.RESET} Withdraw funds                   ║")
                print(f"║  {Color.YELLOW}[5]{Color.RESET} View your crypto                 ║")
                print(f"║  {Color.YELLOW}[6]{Color.RESET} Back                             ║")
                print("╚═══════════════════════════════════════╝")
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
                    active_wallet.withdraw()
                elif sub_choice == "5":
                    clear_console()
                    active_wallet.view_all_crypto()
                elif sub_choice == "6":
                    break
                else:
                    print(f"{Color.RED}Invalid input, please try again.{Color.RESET}")
                time.sleep(1)
        
        elif choice == "8":
            clear_console()
            print(f"{Color.RED}Exit...{Color.RESET}")
            if active_wallet:
                active_wallet.save_wallet()
            break
        else:
            print(f"{Color.RED}Invalid input, please try again.{Color.RESET}")
        
        time.sleep(1)