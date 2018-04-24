import json
import requests


class Requester:
    def __init__(self):
        self.url = "http://127.0.0.1:5000"

    def request(self, method, endpoint, params=None):
        url = self.url + endpoint

        if method == "GET":
            r = requests.get(url, params=params)

            return r.text
        else:
            r = requests.post(url, data=params)

            return r.json()

    def login(self, username, real_name):
        endpoint = "/user_exists"
        params = {"username": username, "real_name": real_name}

        user_exists = self.request("POST", endpoint, params)

        if user_exists["exists"]:
            return True

        return False

    def create_account(self, username, real_name):
        endpoint = "/user_exists"
        params = {"username": username}
        exists = self.request("POST", endpoint, params)

        if exists["exists"]:
            return False

        endpoint = "/add_user"
        params = {"username": username, "real_name": real_name}

        self.request("POST", endpoint, params)

        return True

    def get_all_users(self):
        endpoint = "/get_all_users"

        users = self.request("GET", endpoint)
        print(users)

        return json.loads(users)

    def prepare_conversation(self, user_one, user_two):
        endpoint = "/create_conversation_db"
        params = {"user_one": user_one, "user_two": user_two}

        self.request("POST", endpoint, params)

        endpoint = "/get_message_history"
        history = self.request("POST", endpoint, params)

        return history

    def send_message(self, author, friend_name, message):
        endpoint = f"/send_message/{friend_name}"
        params = {
            "author": author,
            "message": message,
        }

        self.request("POST", endpoint, params)

        return True

