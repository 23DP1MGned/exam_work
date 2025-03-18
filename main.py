import os
import time
from app.models.CryptoWallet import CryptoWallet
from app.models.Transactions import Transactions
from app.utils import clear_console

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
        print("5-  Withdraw funds")
        print("6-  View your crypto")
        print("7 - Exit")
        print(" ")
        
        choice = input("Enter action number: ")
        
        if choice == "1":
            clear_console()
            amount = input("Enter the amount in USDT or Enter to return: ")
            if amount == "":
                continue
            else:
                amount = float(amount)
                wallet.top_up(amount)
        elif choice == "2":
            clear_console()
            print(f"Your USDT balance: {wallet.balances.get("USDT", 0)} USDT")
            print(" ")
            crypto = input("Enter Crypto (BTC, ETH, SOL, DOT, TON, DOGE, LTC, XRP, ADA, AVAX) or Enter to return: ").upper()
            if crypto == "":
                continue
            else:
                amount = float(input("Enter the amount in USDT to convert: "))
                wallet.usdt_to_crypto(crypto, amount)
        elif choice == "3":
            clear_console()
            filtered_balances = {currency: amount for currency, amount in wallet.balances.items() if amount > 0 and currency.upper() != "USDT"}
            if filtered_balances:
                print("Your Crypto:")
                print(" ")
                for currency, amount in filtered_balances.items():
                    print(f"{currency}: {amount:.8f}")
            else:
                print("You have no Сrypto on your balance.")
            if filtered_balances:
                print(" ")
                crypto = input("Enter Crypto or Enter to return: ").upper()
                if crypto == "":
                    continue
                else:
                    amount = float(input("Enter the amount to convert: "))
                    wallet.crypto_to_usdt(crypto, amount)
            else:
                print(" ")
                input("Press Enter to return to the main menu...")
        elif choice == "4":
            clear_console()
            Transactions.view_transactions()
        elif choice == "5":
            clear_console()
            print("Available balances:")
            print(" ")
            for currency, amount in wallet.balances.items():
                if amount > 0:
                    print(f"{currency}: {amount:.8f}")
            print(" ")
            currency = input("Enter the crypto to withdraw or Enter to return: ").upper()
            if currency == "":
                continue
            else:
                amount = float(input("Enter the amount to withdraw: "))
                wallet.withdraw(currency, amount)
                time.sleep(2)
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
