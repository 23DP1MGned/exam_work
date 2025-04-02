import os
import json
from app.utils import clear_console

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
        print("No user found. Please register.")
        login = input("Enter your login: ")
        password = input("Enter your password: ")
        User.save_user_data(login, password)
        print("Registration successful!")

    def authenticate():
        clear_console()
        if not User.load_user_data():
            User.register()