import sqlite3


class Database:
    def __init__(self):
        self.database = "chat.db"

    def perform_insert(self, sql, params):
        conn = sqlite3.connect(self.database)
        cursor = conn.cursor()
        cursor.execute(sql, params)
        conn.commit()
        conn.close()

    def perform_select(self, sql, params):
        conn = sqlite3.connect(self.database)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        cursor.execute(sql, params)
        results = [dict(row) for row in cursor.fetchall()]
        conn.close()

        return results

    def add_user(self, username, real_name):
        sql = "INSERT INTO users (username, real_name) VALUES (?,?)"
        query_params = (username, real_name)

        self.perform_insert(sql, query_params)

    def get_all_users(self):
        sql = "SELECT username, real_name, avatar FROM users"
        params = []

        return self.perform_select(sql, params)

    def user_exists(self, username):
        sql = "SELECT username FROM users WHERE username = ?"
        params = (username,)

        results = self.perform_select(sql, params)

        if len(results):
            return True

        return False

    def update_avatar(self, username, img_b64):
        sql = "UPDATE users SET avatar=? WHERE username=?"
        params = (img_b64, username)

        return self.perform_insert(sql, params)

    def get_user_avatar(self, username):
        sql = "SELECT avatar FROM users WHERE username=?"
        params = (username,)

        return self.perform_select(sql, params)

    def add_friend(self, user_one, user_two):
        sql = "INSERT INTO friends (user_one, user_two, blocked) VALUES (?,?,0)"
        query_params = (user_one, user_two)

        self.perform_insert(sql, query_params)

    def get_friends(self, username):
        all_friends = []
        sql = "SELECT user_two FROM friends WHERE user_one=? AND blocked=0"
        params = (username,)
        friends = self.perform_select(sql, params)

        sql = "SELECT user_one FROM friends WHERE user_two=? AND blocked=0"
        friends2 = self.perform_select(sql, params)

        for friend in friends:
            all_friends.append(friend["user_two"])
        for friend in friends2:
            all_friends.append(friend["user_one"])

        return all_friends

    def get_users_by_usernames(self, usernames):
        question_marks = ','.join(['?' for user in usernames])
        sql = f"SELECT * FROM users WHERE username IN ({question_marks})"
        params = [user for user in usernames]

        friends = self.perform_select(sql, params)

        return friends

    def block_friend(self, username, contact_to_block):
        sql = "UPDATE friends SET blocked=1 WHERE (user_one = ? AND user_two = ?) OR (user_two = ? AND user_one = ?)"
        query_params = (username, contact_to_block, username, contact_to_block)

        self.perform_insert(sql, query_params)
