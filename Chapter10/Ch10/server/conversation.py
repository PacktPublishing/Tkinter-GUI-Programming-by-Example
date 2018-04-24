import arrow
import sqlite3


class Conversation:
    def __init__(self, database):
        self.database = database

    def initialise_table(self):
        sql = "CREATE TABLE conversation (author text, message text, date_sent text)"
        conn = sqlite3.connect(self.database)
        cursor = conn.cursor()
        cursor.execute(sql)
        conn.commit()
        conn.close()

    def get_history(self):
        sql = "SELECT * FROM conversation"
        conn = sqlite3.connect(self.database)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        cursor.execute(sql)
        results = [dict(row) for row in cursor.fetchall()]
        conn.close()

        return results

    def add_message(self, author, message, date_sent):
        sql = "INSERT INTO conversation VALUES (?, ?, ?)"
        params = (author, message, date_sent)
        conn = sqlite3.connect(self.database)
        cursor = conn.cursor()
        cursor.execute(sql, params)
        conn.commit()
        conn.close()

    def get_new_messages(self, timestamp, username):
        sql = "SELECT author, message FROM conversation WHERE date_sent > ? AND author <> ?"
        params = (timestamp, username)

        conn = sqlite3.connect(self.database)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        cursor.execute(sql, params)
        results = [dict(row) for row in cursor.fetchall()]
        conn.close()

        return results