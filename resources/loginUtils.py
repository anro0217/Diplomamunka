import re
import bcrypt

def is_valid_email(email):
    pattern = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"
    return re.match(pattern, email) is not None

def get_username_field_type(input_string):
    if is_valid_email(input_string):
        return "email"
    else:
        return "username"

def is_strong_password(password):
    # Legalább 8 karakter, tartalmazhat nagybetűt, kisbetűt, számot és speciális karaktert
    pattern = r"^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[^\w\s])[A-Za-z\d\W]{8,}$"
    return re.match(pattern, password) is not None

def hash_password(password):
    salt = bcrypt.gensalt()
    return bcrypt.hashpw(password.encode('utf-8'), salt)

def check_password(hashed_password, user_password):
    return bcrypt.checkpw(user_password.encode('utf-8'), hashed_password)
