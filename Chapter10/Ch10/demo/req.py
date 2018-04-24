import requests


data = {
    "username": "david",
}
r = requests.post("http://127.0.0.1:5000/user_exists", data=data)

print(r.text)
