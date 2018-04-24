import sqlite3

database = sqlite3.connect("chat.db")
cursor = database.cursor()

create_users_sql = "CREATE TABLE users (username TEXT, real_name TEXT)"
cursor.execute(create_users_sql)

database.commit()
database.close()
