import os
import json


class User:
    def __init__(self, username, password_hash):
        self.username = username
        self.password_hash = password_hash


def load_users():
    if not os.path.exists('users.json'):
        return {}
    with open('users.json', 'r') as f:
        users = json.load(f)
    return users


def save_user(user):
    users = load_users()
    users[user.username] = user.password_hash
    with open('users.json', 'w') as f:
        json.dump(users, f)
