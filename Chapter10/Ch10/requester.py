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

    def get_user_avatar(self, username):
        endpoint = f"/get_user_avatar/{username}"

        avatar = self.request("GET", endpoint)

        return json.loads(avatar)

    def update_avatar(self, username, img_b64):
        endpoint = f"/update_avatar/{username}"
        params = {
            "img_b64": img_b64
        }

        self.request("POST", endpoint, params)

        return True

    def get_new_messages(self, timestamp, user_one, user_two):
        """ user_one is the author's username, and user_two is the friend's """
        endpoint = "/get_new_messages"
        params = {
            "timestamp": timestamp,
            "user_one": user_one,
            "user_two": user_two,
        }

        new_messages = self.request("POST", endpoint, params)

        return new_messages

    def add_friend(self, user_one, user_two):
        endpoint = "/add_friend"
        params = {
            "user_one": user_one,
            "user_two": user_two,
        }

        success = self.request("POST", endpoint, params)

        return success["success"]

    def get_friends(self, username):
        endpoint = f"/get_friends/{username}"

        friends = self.request("GET", endpoint)

        return json.loads(friends)

    def block_friend(self, user_one, user_two):
        endpoint = "/block_friend"
        params = {
            "user_one": user_one,
            "user_two": user_two,
        }

        self.request("POST", endpoint, params)

        return True
