import sqlite3

from resources.utils import loginUtils


class DatabaseManager:
    def __init__(self, db_file):
        self.db_file = db_file
        self.conn = sqlite3.connect(db_file)
        self.cursor = self.conn.cursor()
        self.init_db()

    def init_db(self):
        conn = sqlite3.connect(self.db_file)
        c = conn.cursor()

        # # Ellenőrizzük, hogy az oszlop már létezik-e
        # c.execute('PRAGMA table_info(tasks)')
        # columns = [row[1] for row in c.fetchall()]
        #
        # if 'material' not in columns:
        #     # Ha az oszlop nem létezik, hozzáadjuk
        #     c.execute('ALTER TABLE tasks ADD COLUMN material TEXT')

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
                correct_code TEXT,
                material TEXT
            )
        ''')
        # Kapcsolótábla létrehozása a felhasználók és feladatok között
        c.execute('''
            CREATE TABLE IF NOT EXISTS user_tasks (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                task_id INTEGER NOT NULL,
                status INTEGER NOT NULL DEFAULT 0,
                failures INTEGER NOT NULL DEFAULT 0,
                FOREIGN KEY(user_id) REFERENCES users(id),
                FOREIGN KEY(task_id) REFERENCES tasks(id),
                UNIQUE(user_id, task_id)
            )
        ''')

        c.execute('''
            CREATE TABLE IF NOT EXISTS user_settings (
                        id INTEGER PRIMARY KEY,
                        user_id TEXT UNIQUE,
                        theme TEXT,
                        font_size INTEGER
            )
        ''')

        # c.execute('''DROP TABLE user_tasks''')

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
        if loginUtils.get_username_field_type(username_or_email) == "email":
            c.execute("SELECT id, password FROM users WHERE email = ?", (username_or_email,))
        else:
            c.execute("SELECT id, password FROM users WHERE username = ?", (username_or_email,))
        user = c.fetchone()
        conn.close()
        if user and loginUtils.check_password(user[1], password):
            return user[0]
        return None

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
                 correct_code=None, material=None):
        try:
            conn = sqlite3.connect(self.db_file)
            c = conn.cursor()

            # Legkisebb szabad ID keresése
            c.execute('''
                SELECT COALESCE(MIN(t1.id + 1), 1) 
                FROM tasks t1 
                LEFT JOIN tasks t2 ON t1.id + 1 = t2.id 
                WHERE t2.id IS NULL
            ''')
            next_id = c.fetchone()[0]

            # Feladat hozzáadása a következő szabad ID-val
            c.execute('''
                INSERT INTO tasks (id, title, description, type, code_template, code_result, drag_drop_items, 
                matching_pairs, quiz_question, quiz_options, quiz_answer, debugging_code, correct_code, material)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (next_id, title, description, task_type, code_template, code_result, drag_drop_items, matching_pairs,
                  quiz_question, quiz_options, quiz_answer, debugging_code, correct_code, material))
            conn.commit()
        except sqlite3.Error as e:
            print("Database error:", e)
            return False
        finally:
            conn.close()
        return True

    def update_task(self, task_id, title, description, task_type, code_template=None, code_result=None,
                    drag_drop_items=None, matching_pairs=None, quiz_question=None, quiz_options=None,
                    quiz_answer=None, debugging_code=None, correct_code=None, material=None):
        try:
            conn = sqlite3.connect(self.db_file)
            c = conn.cursor()

            c.execute('''
                UPDATE tasks
                SET title = ?, description = ?, type = ?, code_template = ?, code_result = ?, 
                    drag_drop_items = ?, matching_pairs = ?, quiz_question = ?, quiz_options = ?, 
                    quiz_answer = ?, debugging_code = ?, correct_code = ?, material = ?
                WHERE id = ?
            ''', (title, description, task_type, code_template, code_result, drag_drop_items,
                  matching_pairs, quiz_question, quiz_options, quiz_answer, debugging_code, correct_code, material,
                  task_id))
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
            quiz_question, quiz_options, quiz_answer, debugging_code, correct_code, material
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
            quiz_question, quiz_options, quiz_answer, debugging_code, correct_code, material
            FROM tasks WHERE id = ?
        ''', (task_id,))
        task = c.fetchone()
        conn.close()
        return dict(task) if task else None

    def get_task_by_title(self, title):
        try:
            conn = sqlite3.connect(self.db_file)
            c = conn.cursor()
            c.execute("SELECT * FROM tasks WHERE title = ?", (title,))
            return c.fetchone()
        except sqlite3.Error as e:
            print("Database error:", e)
            return None
        finally:
            conn.close()

    def regenerate_ids(self):
        conn = sqlite3.connect(self.db_file)
        c = conn.cursor()
        c.execute('''CREATE TABLE IF NOT EXISTS temp_tasks AS SELECT * FROM tasks ORDER BY id ASC''')
        c.execute('''DELETE FROM tasks''')
        c.execute('''UPDATE sqlite_sequence SET seq = 0 WHERE name = 'tasks' ''')
        c.execute('''INSERT INTO tasks (title, description, type, code_template, code_result, drag_drop_items, 
                    matching_pairs, quiz_question, quiz_options, quiz_answer, debugging_code, correct_code, material)
                    SELECT title, description, type, code_template, code_result, drag_drop_items, 
                    matching_pairs, quiz_question, quiz_options, quiz_answer, debugging_code, correct_code, material
                    FROM temp_tasks''')
        c.execute('''DROP TABLE temp_tasks''')
        conn.commit()
        conn.close()

    def delete(self, table_name, record_ids):
        try:
            conn = sqlite3.connect(self.db_file)
            c = conn.cursor()

            # Kapcsolódó rekordok törlése a user_tasks táblából
            if table_name == "tasks":
                placeholders = ', '.join(['?'] * len(record_ids))  # Kérdőjelek generálása
                c.execute(f"DELETE FROM user_tasks WHERE task_id IN ({placeholders})", record_ids)
            elif table_name == "users":
                placeholders = ', '.join(['?'] * len(record_ids))  # Kérdőjelek generálása
                c.execute(f"DELETE FROM user_tasks WHERE user_id IN ({placeholders})", record_ids)

            # Rekordok törlése a fő táblából
            placeholders = ', '.join(['?'] * len(record_ids))  # Kérdőjelek generálása
            query = f"DELETE FROM {table_name} WHERE id IN ({placeholders})"
            c.execute(query, record_ids)
            conn.commit()

            if table_name == "tasks":
                self.reindex_tasks()
            elif table_name == "users":
                self.reindex_users()
            elif table_name == "user_tasks":
                self.reindex_user_tasks()

        except sqlite3.Error as e:
            print(f"Database error: {e}")
            return False
        finally:
            conn.close()
        return True

    def reindex_tasks(self):
        conn = sqlite3.connect(self.db_file)
        c = conn.cursor()

        # Létrehozunk egy ideiglenes táblát az újraindexeléshez
        c.execute('''
            CREATE TEMPORARY TABLE tasks_temp AS 
            SELECT rowid AS old_id, * FROM tasks ORDER BY id ASC
        ''')

        # Töröljük az eredeti feladatokat
        c.execute('DELETE FROM tasks')
        c.execute('DELETE FROM sqlite_sequence WHERE name="tasks"')

        # Beszúrjuk az újraindexelt feladatokat
        c.execute('''
            INSERT INTO tasks (title, description, type, code_template, code_result, drag_drop_items, 
                matching_pairs, quiz_question, quiz_options, quiz_answer, debugging_code, correct_code, material)
            SELECT title, description, type, code_template, code_result, drag_drop_items, 
                matching_pairs, quiz_question, quiz_options, quiz_answer, debugging_code, correct_code, material
            FROM tasks_temp
        ''')

        # Frissítjük a user_tasks táblát
        c.execute('''
            UPDATE user_tasks 
            SET task_id = (
                SELECT tasks.id 
                FROM tasks 
                JOIN tasks_temp ON tasks_temp.old_id = user_tasks.task_id
                WHERE tasks_temp.old_id = user_tasks.task_id
            )
            WHERE EXISTS (SELECT 1 FROM tasks_temp WHERE tasks_temp.old_id = user_tasks.task_id)
        ''')

        # Töröljük az ideiglenes táblát
        c.execute('DROP TABLE tasks_temp')
        conn.commit()
        conn.close()

    def reindex_users(self):
        conn = sqlite3.connect(self.db_file)
        c = conn.cursor()

        # Létrehozunk egy ideiglenes táblát az újraindexeléshez
        c.execute('''
            CREATE TEMPORARY TABLE users_temp AS 
            SELECT rowid AS old_id, * FROM users ORDER BY id ASC
        ''')

        # Töröljük az eredeti felhasználókat
        c.execute('DELETE FROM users')
        c.execute('DELETE FROM sqlite_sequence WHERE name="users"')

        # Beszúrjuk az újraindexelt felhasználókat
        c.execute('''
            INSERT INTO users (username, email, password)
            SELECT username, email, password
            FROM users_temp
        ''')

        # Frissítjük a user_tasks táblát
        c.execute('''
            UPDATE user_tasks 
            SET user_id = (
                SELECT users.id 
                FROM users 
                JOIN users_temp ON users_temp.old_id = user_tasks.user_id
                WHERE users_temp.old_id = user_tasks.user_id
            )
            WHERE EXISTS (SELECT 1 FROM users_temp WHERE users_temp.old_id = user_tasks.user_id)
        ''')

        # Töröljük az ideiglenes táblát
        c.execute('DROP TABLE users_temp')
        conn.commit()
        conn.close()

    def reindex_user_tasks(self):
        conn = sqlite3.connect(self.db_file)
        c = conn.cursor()

        # Létrehozunk egy ideiglenes táblát az újraindexeléshez
        c.execute('''
            CREATE TEMPORARY TABLE user_tasks_temp AS 
            SELECT rowid AS old_id, * FROM user_tasks ORDER BY id ASC
        ''')

        # Töröljük az eredeti user_tasks rekordokat
        c.execute('DELETE FROM user_tasks')
        c.execute('DELETE FROM sqlite_sequence WHERE name="user_tasks"')

        # Beszúrjuk az újraindexelt user_tasks rekordokat
        c.execute('''
            INSERT INTO user_tasks (user_id, task_id, status)
            SELECT user_id, task_id, status
            FROM user_tasks_temp
        ''')

        # Töröljük az ideiglenes táblát
        c.execute('DROP TABLE user_tasks_temp')
        conn.commit()
        conn.close()

    def mark_task_as_completed(self, user_id, task_id):
        try:
            conn = sqlite3.connect(self.db_file)
            c = conn.cursor()
            existing_record = c.execute(
                'SELECT failures FROM user_tasks WHERE user_id = ? AND task_id = ?',
                (user_id, task_id)
            ).fetchone()

            if existing_record:
                c.execute('''
                    UPDATE user_tasks 
                    SET status = 1 
                    WHERE user_id = ? AND task_id = ?
                ''', (user_id, task_id))
            else:
                c.execute('''
                    INSERT INTO user_tasks (user_id, task_id, status, failures) 
                    VALUES (?, ?, 1, 0)
                ''', (user_id, task_id))

            conn.commit()
        except sqlite3.Error as e:
            print("Database error:", e)
            return False
        finally:
            conn.close()
        return True

    def increment_failure_count(self, user_id, task_id):
        try:
            conn = sqlite3.connect(self.db_file)
            c = conn.cursor()
            existing_record = c.execute(
                'SELECT failures FROM user_tasks WHERE user_id = ? AND task_id = ?',
                (user_id, task_id)
            ).fetchone()

            if existing_record:
                c.execute('''
                    UPDATE user_tasks 
                    SET failures = failures + 1 
                    WHERE user_id = ? AND task_id = ?
                ''', (user_id, task_id))
            else:
                c.execute('''
                    INSERT INTO user_tasks (user_id, task_id, status, failures) 
                    VALUES (?, ?, 0, 1)
                ''', (user_id, task_id))

            conn.commit()
        except sqlite3.Error as e:
            print("Database error:", e)
            return False
        finally:
            conn.close()
        return True

    def get_completed_tasks(self, user_id):
        query = 'SELECT task_id FROM user_tasks WHERE user_id = ? AND status = 1'
        self.cursor.execute(query, (user_id,))
        rows = self.cursor.fetchall()
        return [row[0] for row in rows]

    def get_user_id_by_username_or_email(self, username_or_email):
        conn = sqlite3.connect(self.db_file)
        c = conn.cursor()
        if loginUtils.get_username_field_type(username_or_email) == "email":
            c.execute("SELECT id FROM users WHERE email = ?", (username_or_email,))
        else:
            c.execute("SELECT id FROM users WHERE username = ?", (username_or_email,))
        user_id = c.fetchone()
        conn.close()
        return user_id[0] if user_id else None

    def save_user_settings(self, user_id, theme=None, font_size=None):
        conn = sqlite3.connect(self.db_file)
        c = conn.cursor()

        c.execute("SELECT theme, font_size FROM user_settings WHERE user_id=?", (user_id,))
        result = c.fetchone()

        if result:
            current_theme, current_font_size = result  # A jelenlegi beállítások

            # Csak akkor frissítjük, ha az új beállítások eltérnek a régiektől
            updated = False
            if theme is not None and theme != current_theme:
                current_theme = theme
                updated = True
            if font_size is not None and font_size != current_font_size:
                current_font_size = font_size
                updated = True

            if updated:
                c.execute("UPDATE user_settings SET theme=?, font_size=? WHERE user_id=?",
                          (current_theme, current_font_size, user_id))

        else:
            # Új beállításokat adunk hozzá, ha egyik sem létezik
            c.execute("INSERT INTO user_settings (user_id, theme, font_size) VALUES (?, ?, ?)",
                      (user_id, theme if theme is not None else 'light', font_size if font_size is not None else 10))

        conn.commit()
        conn.close()

    def load_user_settings(self, user_id):
        conn = sqlite3.connect(self.db_file)
        c = conn.cursor()

        c.execute("SELECT theme, font_size FROM user_settings WHERE user_id=?", (user_id,))
        result = c.fetchone()

        conn.close()

        if result:
            return {
                'theme': result[0],
                'font_size': result[1]
            }
        else:
            return None

    def get_user_statistics(self, user_id):
        conn = sqlite3.connect(self.db_file)
        c = conn.cursor()

        c.execute("SELECT task_id, status, failures FROM user_tasks WHERE user_id = ?", (user_id,))
        results = c.fetchall()
        c.execute("SELECT COUNT(*) FROM tasks")
        total_tasks = c.fetchone()[0]
        conn.close()

        # Összesített statisztikák kiszámítása
        completed_tasks = sum(1 for task in results if task[1] == 1)  # Teljesített feladatok
        total_failures = sum(task[2] for task in results)  # Összes hiba

        # Teljesítési arány és pontosság kiszámítása
        completion_rate = (completed_tasks / total_tasks * 100) if total_tasks > 0 else 0
        accuracy = (completed_tasks / (
                completed_tasks + total_failures) * 100) if completed_tasks + total_failures > 0 else 0

        return {
            "total_tasks": total_tasks,
            "completed_tasks": completed_tasks,
            "total_failures": total_failures,
            "completion_rate": completion_rate,
            "accuracy": accuracy
        }

    def get_user_tasks(self, user_id):
        conn = sqlite3.connect(self.db_file)
        c = conn.cursor()

        c.execute("SELECT t.id, t.title, ut.status, ut.failures FROM user_tasks ut JOIN tasks t ON ut.task_id = t.id "
                  "WHERE ut.user_id = ?", (user_id,))
        results = c.fetchall()
        conn.close()

        return results
