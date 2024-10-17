import os
import re
import bcrypt
import sys

# Futtatási könyvtár meghatározása (ahonnan az exe fut)
if getattr(sys, 'frozen', False):
    application_path = os.path.dirname(sys.executable)  # Az exe futtatási könyvtára
else:
    application_path = os.path.dirname(os.path.abspath(__file__))  # Fejlesztési környezet

# A login_state.cfg elérési útja
config_file_path = os.path.join(application_path, 'login_state.cfg')

def is_valid_email(email):
    pattern = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"
    return re.match(pattern, email) is not None

def get_username_field_type(input_string):
    if is_valid_email(input_string):
        return "email"
    else:
        return "username"

def is_strong_password(password):
    pattern = r"^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[^\w\s_])[A-Za-z\d\W_]{8,}$"
    return re.match(pattern, password) is not None

def hash_password(password):
    salt = bcrypt.gensalt()
    return bcrypt.hashpw(password.encode('utf-8'), salt)

def check_password(hashed_password, user_password):
    return bcrypt.checkpw(user_password.encode('utf-8'), hashed_password)

def is_email(string):
    return "@" in string and "." in string

def save_login_state(username):
    with open(config_file_path, 'w', encoding='utf-8') as f:
        username = '\u200B'.join(username)
        f.write(username)

def delete_login_state():
    try:
        os.remove(config_file_path)
    except FileNotFoundError:
        pass
