import sqlite3

from resources.utils import loginUtils


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
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                description TEXT NOT NULL,
                type TEXT NOT NULL,
                code_template TEXT,
                code_result TEXT,
                drag_drop_items TEXT,
                matching_pairs TEXT,
                quiz_question TEXT,
                quiz_options TEXT,
                quiz_answer TEXT,
                debugging_code TEXT,
                correct_code TEXT
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

        # Oszlopcímek lekérése
        columns = [description[0] for description in c.description]

        conn.close()
        return data, columns

    def add_task(self, title, description, task_type, code_template=None, code_result=None, drag_drop_items=None,
                 matching_pairs=None, quiz_question=None, quiz_options=None, quiz_answer=None, debugging_code=None,
                 correct_code=None):
        try:
            conn = sqlite3.connect(self.db_file)
            c = conn.cursor()
            c.execute('''
                INSERT INTO tasks (title, description, type, code_template, code_result, drag_drop_items, 
                matching_pairs, quiz_question, quiz_options, quiz_answer, debugging_code, correct_code)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''',
                      (title, description, task_type, code_template, code_result, drag_drop_items, matching_pairs,
                       quiz_question,
                       quiz_options, quiz_answer, debugging_code, correct_code))
            conn.commit()
        except sqlite3.Error as e:
            print("Database error:", e)
            return False
        finally:
            conn.close()
        return True

    def get_task(self, title):
        conn = sqlite3.connect(self.db_file)
        conn.row_factory = sqlite3.Row  # Eredmények szótárként való visszaadása
        c = conn.cursor()
        c.execute('''
            SELECT title, description, type, code_template, code_result, drag_drop_items, matching_pairs, 
            quiz_question, quiz_options, quiz_answer, debugging_code, correct_code
            FROM tasks WHERE title = ?
        ''', (title,))
        task = c.fetchone()
        conn.close()
        return dict(task) if task else None

    def get_tasks(self):
        conn = sqlite3.connect(self.db_file)
        conn.row_factory = sqlite3.Row  # Eredmények szótárként való visszaadása
        c = conn.cursor()
        c.execute("SELECT id, title FROM tasks ORDER BY id ASC")
        tasks = c.fetchall()
        conn.close()
        return [{'id': task['id'], 'title': task['title']} for task in tasks]

    def get_task_by_id(self, task_id):
        conn = sqlite3.connect(self.db_file)
        conn.row_factory = sqlite3.Row  # Eredmények szótárként való visszaadása
        c = conn.cursor()
        c.execute('''
            SELECT id, title, description, type, code_template, code_result, drag_drop_items, matching_pairs, 
            quiz_question, quiz_options, quiz_answer, debugging_code, correct_code
            FROM tasks WHERE id = ?
        ''', (task_id,))
        task = c.fetchone()
        conn.close()
        return dict(task) if task else None

    def regenerate_ids(self):
        conn = sqlite3.connect(self.db_file)
        c = conn.cursor()
        c.execute('''CREATE TABLE IF NOT EXISTS temp_tasks AS SELECT * FROM tasks ORDER BY id ASC''')
        c.execute('''DELETE FROM tasks''')
        c.execute('''UPDATE sqlite_sequence SET seq = 0 WHERE name = 'tasks' ''')
        c.execute('''INSERT INTO tasks (title, description, type, code_template, code_result, drag_drop_items, 
                    matching_pairs, quiz_question, quiz_options, quiz_answer, debugging_code, correct_code)
                    SELECT title, description, type, code_template, code_result, drag_drop_items, 
                    matching_pairs, quiz_question, quiz_options, quiz_answer, debugging_code, correct_code
                    FROM temp_tasks''')
        c.execute('''DROP TABLE temp_tasks''')
        conn.commit()
        conn.close()

    def delete(self, table_name, record_id):
        try:
            conn = sqlite3.connect(self.db_file)
            c = conn.cursor()
            query = f"DELETE FROM {table_name} WHERE id = ?"
            c.execute(query, (record_id,))
            conn.commit()
            if table_name == "tasks":
                self.regenerate_ids()  # Újragenerálja az ID-kat a törlés után
        except sqlite3.Error as e:
            print(f"Database error: {e}")
            return False
        finally:
            conn.close()
        return True

