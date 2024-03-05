import sqlite3
import os


from resources import loginUtils


class DatabaseManager:
    def __init__(self, db_file):
        self.db_file = db_file
        self.init_db()

    def init_db(self):
        conn = sqlite3.connect(self.db_file)
        c = conn.cursor()
        c.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY,
                username TEXT UNIQUE NOT NULL,
                email TEXT UNIQUE NOT NULL,
                password TEXT NOT NULL
            )
        ''')
        # Feladatok táblájának létrehozása
        c.execute('''
                    CREATE TABLE IF NOT EXISTS tasks (
                        id INTEGER PRIMARY KEY,
                        title TEXT NOT NULL,
                        description TEXT NOT NULL,
                        solution TEXT NOT NULL
                    )
                ''')
        # Kapcsolótábla létrehozása a felhasználók és feladatok között
        c.execute('''
                    CREATE TABLE IF NOT EXISTS user_tasks (
                        user_id INTEGER NOT NULL,
                        task_id INTEGER NOT NULL,
                        status INTEGER NOT NULL DEFAULT 0,
                        FOREIGN KEY(user_id) REFERENCES users(id),
                        FOREIGN KEY(task_id) REFERENCES tasks(id),
                        PRIMARY KEY(user_id, task_id)
                    )
                ''')
        conn.commit()
        conn.close()

    def add_user(self, username, email, password):
        if self.user_exists(username, email):
            print("Username already exists")
            return False
        try:
            conn = sqlite3.connect(self.db_file)
            c = conn.cursor()
            c.execute("INSERT INTO users (username, email, password) VALUES (?, ?, ?)",
                      (username, email, password))
            conn.commit()
        except sqlite3.Error as e:
            print("Database error:", e)
            return False
        finally:
            conn.close()
        return True

    def user_exists(self, username, email):
        conn = sqlite3.connect(self.db_file)
        c = conn.cursor()
        c.execute("SELECT * FROM users WHERE username = ? OR email = ?", (username, email))
        user = c.fetchone()
        conn.close()
        return user is not None

    def get_username_by_email(self, email):
        conn = sqlite3.connect(self.db_file)
        c = conn.cursor()
        c.execute("SELECT username FROM users WHERE email = ?", (email,))
        result = c.fetchone()
        conn.close()
        if result:
            return result[0]
        return None

    def validate_login(self, username_or_email, password):
        conn = sqlite3.connect(self.db_file)
        c = conn.cursor()
        if loginUtils.get_username_field_type(username_or_email) == "email":  # Email cím esetén
            c.execute("SELECT password FROM users WHERE email = ?", (username_or_email,))
        else:  # Felhasználónév esetén
            c.execute("SELECT password FROM users WHERE username = ?", (username_or_email,))
        stored_password = c.fetchone()
        conn.close()
        if stored_password and loginUtils.check_password(stored_password[0], password):
            return True
        return False

    def get_table_names(self):
        conn = sqlite3.connect(self.db_file)
        c = conn.cursor()
        c.execute("SELECT name FROM sqlite_master WHERE type='table';")
        tables = [table[0] for table in c.fetchall()]
        conn.close()
        return tables

    def get_table_data(self, table_name):
        conn = sqlite3.connect(self.db_file)
        c = conn.cursor()
        c.execute(f"SELECT * FROM {table_name};")
        data = c.fetchall()
        conn.close()
        return data

    def add_task(self, title, description, solution):
        try:
            conn = sqlite3.connect(self.db_file)
            c = conn.cursor()
            c.execute("INSERT INTO tasks (title, description, solution) VALUES (?, ?, ?)",
                      (title, description, solution))
            conn.commit()
        except sqlite3.Error as e:
            print("Database error:", e)
            return False
        finally:
            conn.close()
        return True
