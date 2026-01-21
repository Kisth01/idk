from pathlib import Path
import json
def get_stored_usermane(path):
    if path.exists():
        contents = path.read_text()
        usermane = json.loads(contents)
        return usermane
    else:
        return None

def get_new_username(path):
    username = input("What's your name?")
    contents = json.dumps(username)
    path.write_text(contents)
    return username

def greet_user():
    path = Path('username.json')
    username = get_stored_usermane(path)
    if username:
        print(f'Welcome back, {username}')
    else:
        username = get_new_username()
        print(f"We'll remember you when you come back, {username}")

greet_user()