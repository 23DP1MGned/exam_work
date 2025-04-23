> Autor: Maksims Gnedovs

# Cryptocurrency Wallet

A simple console crypto wallet application built with Python 3. This project allows users to manage their crypto assets, check balances, make transactions, top up in euros (automatically converting to USDT), convert between different crypto, and transfer funds between user's own wallets .

---

## Wallet Features

- **User registration and authentication**
- **Wallets creation** (users can have multiple wallets)
- **Top up with euros** — automatically converted to BTC
- **Currency conversion** — for example: BTC to ETH
- **Send funds** — between user's own wallets
- **Transaction history** — stored in `user_transactions.json`
- **Data stored using JSON files**

---

## Project Structure
exam_work-main/
├── app/                       # Application logic (services, utilities, etc.)
├── main.py                   # Main entry point of the application
├── app_main.py               # Main user interface/controller of the app
├── user_data.json            # User data
├── user_transactions.json    # All user transactions
├── wallets/                  # Wallet files
├── tests/                    # Unit tests
├── requirements.txt          # List of dependencies
└── README. md                 # Documentation


