import os
import arrow

from flask import Flask, session, url_for, request, g, jsonify, json

from database import Database
from conversation import Conversation


app = Flask(__name__)
app.config.from_object(__name__)

app.secret_key = "tkinterguiprogrammingbyexample"

database = Database()

conversations_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), 'conversations/'))


@app.route("/", methods=["GET"])
def index():
    data = {
        "cats": 5,
        "people": 8,
        "dogs": 4
    }

    return jsonify(data)


@app.route("/send_me_data", methods=["POST"])
def send_me_data():
    data = request.form
    for key, value in data.items():
        print("received", key, "with value", value)

    return "Thanks"


@app.route("/get_all_users")
def get_all_users():
    all_users = database.get_all_users()

    return jsonify(all_users)


@app.route("/add_user", methods=["POST"])
def add_user():
    data = request.form
    username = data["username"]
    real_name = data["real_name"]

    database.add_user(username, real_name)

    return jsonify(
        "User Created"
    )


@app.route("/user_exists", methods=["POST"])
def user_exists():
    username = request.form.get("username")
    exists = database.user_exists(username)

    return jsonify({
        "exists": exists
    })


@app.route("/create_conversation_db", methods=["POST"])
def create_conversation_db():
    conversation_db_path = get_conversation_db_path_for_users(request.form)
    print(conversations_dir)

    if not os.path.exists(conversation_db_path):
        with open(conversation_db_path, 'w') as f:
            pass
        conversation = Conversation(conversation_db_path)
        conversation.initialise_table()

    return jsonify({
        "success": True,
    })


@app.route("/get_message_history", methods=["POST"])
def get_message_history():
    conversation_db_path = get_conversation_db_path_for_users(request.form)
    conversation = Conversation(conversation_db_path)

    history = conversation.get_history()

    return jsonify({
        "history": history
    })


@app.route("/send_message/<username>", methods=["POST"])
def send_message(username):
    data = request.form
    author = data["author"]
    message = data["message"]
    date_sent = arrow.now().timestamp

    conversation_db_path = get_conversation_db_path_for_users({"user_one": author, "user_two": username})
    conversation = Conversation(conversation_db_path)
    conversation.add_message(author, message, date_sent)

    return jsonify({
        "success": True
    })


@app.route("/add_friend", methods=["POST"])
def add_contact():
    data = request.form
    username = data['username']


@app.route("/block_user/<username>")
def block_contact(username):
    pass


@app.route("/unblock_user/<username>")
def unblock_contact(username):
    pass


def get_conversation_db_path_for_users(data):
    user_one = data["user_one"]
    user_two = data["user_two"]

    users_in_order = sorted([user_one, user_two])
    users_in_order = "_".join(users_in_order)

    conversation_db = users_in_order + ".db"
    conversation_db_path = os.path.join(conversations_dir, conversation_db)

    return conversation_db_path

if __name__ == '__main__':
    app.run(debug=True)
