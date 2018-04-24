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
        sql = "SELECT username, real_name FROM users"
        params = []

        return self.perform_select(sql, params)

    def user_exists(self, username):
        sql = "SELECT username FROM users WHERE username = ?"
        params = (username,)

        results = self.perform_select(sql, params)

        if len(results):
            return True

        return False

    def block_contact(self, username, contact_to_block):
        sql = "update relationship set blocked=1 where (user_one = ? and user_two = ?) or (user_two = ? and user_one = ?)"
        query_params = (username, contact_to_block, username, contact_to_block)

        self.perform_insert(sql, query_params)

    def create_relationship(self, user_one, user_two):
        sql = "insert into relationship (user_one, user_two, blocked) values (?,?,0)"
        query_params = (user_one, user_two)

        self.perform_insert(sql, query_params)