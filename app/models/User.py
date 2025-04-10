import os
import json
from app.utils import clear_console
from app.interfaces import Color
import time
from app.interfaces import registr

class User:
    user_file = "user_data.json"
    
    def load_user_data():
        if os.path.exists(User.user_file):
            with open(User.user_file, "r") as file:
                return json.load(file)
        return None

    def save_user_data(login, password):
        with open(User.user_file, "w") as file:
            json.dump({"login": login, "password": password}, file)

    def register():
        print(f"{Color.RED}No user found.{Color.RESET} {Color.GREEN}Please register.{Color.RESET}")
        login = input("Enter your login: ")
        password = input("Enter your password: ")
        User.save_user_data(login, password)
        print(f"{Color.GREEN}Registration successful!{Color.RESET}")
        time.sleep(2)

    def authenticate():
        clear_console()
        if not User.load_user_data():
            registr()
            User.register()