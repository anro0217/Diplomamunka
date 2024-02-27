import sqlite3

from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QVBoxLayout, QLineEdit, QPushButton, QLabel, QFrame
from PyQt5.QtCore import Qt
from basePage import FramelessWindow
from resources.globalSignals import globalSignals


class RegistrationWindow(FramelessWindow):
    def __init__(self, login_window=None):
        super().__init__()
        self.login_window = login_window
        globalSignals.fontSizeChanged.connect(self.setFontSize)
        globalSignals.themeChanged.connect(self.setTheme)
        self.initUI()
        self.setFontSize(10)

    def initUI(self):
        self.layout = QVBoxLayout()

        # Felhasználónév mező
        self.username_field = QLineEdit()
        self.username_field.setPlaceholderText("Username")
        self.layout.addWidget(self.username_field)

        # E-mail mező
        self.email_field = QLineEdit()
        self.email_field.setPlaceholderText("Email")
        self.layout.addWidget(self.email_field)

        # Jelszó létrehozási mező
        self.password_field = QLineEdit()
        self.password_field.setPlaceholderText("Create password")
        self.password_field.setEchoMode(QLineEdit.Password)
        self.layout.addWidget(self.password_field)

        # Jelszó megerősítési mező
        self.confirm_password_field = QLineEdit()
        self.confirm_password_field.setPlaceholderText("Confirm password")
        self.confirm_password_field.setEchoMode(QLineEdit.Password)
        self.layout.addWidget(self.confirm_password_field)

        # Regisztrációs gomb
        self.register_button = QPushButton('Sign up')
        self.register_button.setStyleSheet('font-size: 16px;')
        self.register_button.clicked.connect(self.register)
        self.layout.addWidget(self.register_button)

        # Már van fiók? Bejelentkezés link
        self.login_label = QLabel('Already have an account? <a href="signup">Login</a>', self)
        self.login_label.setAlignment(Qt.AlignCenter)
        self.login_label.setStyleSheet('margin-top: 10px;')
        self.login_label.linkActivated.connect(self.open_login)
        self.layout.addWidget(self.login_label)

        # Divider vonal
        self.divider = QFrame()
        self.divider.setFrameShape(QFrame.HLine)
        self.divider.setFrameShadow(QFrame.Sunken)
        self.layout.addWidget(self.divider)

        self.setLayout(self.layout)
        self.center_window()

    def open_login(self):
        self.hide()
        self.login_window.show()

    def setTheme(self, darkModeEnabled):
        if darkModeEnabled:
            self.setStyleSheet("background-color: #333333; color: #ffffff;")
        else:
            self.setStyleSheet("background-color: #ffffff; color: #000000;")

    def setFontSize(self, size):
        font = self.font()
        font.setPointSize(size)
        self.username_field.setFont(font)
        self.email_field.setFont(font)
        self.password_field.setFont(font)
        self.confirm_password_field.setFont(font)
        self.register_button.setFont(font)

    def register_field_test(self):
        username = self.username_field.text()
        email = self.email_field.text()
        password = self.password_field.text()
        confirm_password = self.confirm_password_field.text()
        print(username + email + password + confirm_password)
    def register(self):
        username = self.username_field.text()
        email = self.email_field.text()
        password = self.password_field.text()
        confirm_password = self.confirm_password_field.text()

        if password != confirm_password:
            print("A megadott jelszavak eltérnek!")
            return

        # Adatbázis kapcsolat létrehozása
        conn = sqlite3.connect('database/application.db')
        c = conn.cursor()

        try:
            # Felhasználónév és email ellenőrzése
            c.execute("SELECT * FROM users WHERE username = ? OR email = ?", (username, email))
            if c.fetchone():
                print("A felhasználónév vagy az email már foglalt!")
                conn.close()
                return

        except sqlite3.Error as e:
            print("Adatbázis hiba:", e)
            print("Hiba típusa:", type(e))

        # Új felhasználó hozzáadása az adatbázishoz
        try:
            c.execute("INSERT INTO users (username, email, password) VALUES (?, ?, ?)", (username, email, password))
            conn.commit()
            print("A regisztráció sikeres!")
        except sqlite3.Error as e:
            print("Adatbázis hiba:", e)
        finally:
            conn.close()

