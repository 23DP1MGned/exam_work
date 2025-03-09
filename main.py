from app.models.CryptoWallet import CryptoWallet
from os import system
from time import sleep

def main():
    user_wallet = CryptoWallet("user1")
    
    while True:
        print("Select an action:")
        print("1 - Top up your balance (EUR)")
        print("2 - Convert EUR to BTC")
        print("3 - Exit")
        
        choice = input("Enter action number: ")
        
        if choice == "1":
            amount = float(input("Enter the replenishment amount in EUR: "))
            user_wallet.top_up(amount)
        elif choice == "2":
            amount = float(input("Enter the amount to convert to BTC (EUR): "))
            user_wallet.convert_to_btc(amount)
        elif choice == "3":
            print("Exit...")
            user_wallet.save_to_file()
            break
        else:
            print("Invalid input, please try again.")

if __name__ == "__main__":
    main()
