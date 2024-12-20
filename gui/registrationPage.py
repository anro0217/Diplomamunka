from PyQt5.QtWidgets import QVBoxLayout, QLineEdit, QPushButton, QLabel, QFrame
from PyQt5.QtCore import Qt
from basePage import FramelessPage
from resources.utils import loginUtils
from resources.utils.globalSignals import globalSignals
from resources.widgets.myPasswordField import PasswordLineEdit


class RegistrationWindow(FramelessPage):
    def __init__(self, login_window):
        super().__init__()
        self.login_window = login_window
        self.initUI()
        self.setFontSize(10)
        globalSignals.fontSizeChanged.connect(self.setFontSize)
        globalSignals.themeChanged.connect(self.setTheme)

    def initUI(self):
        self.layout = QVBoxLayout()

        # Felhasználónév mező
        self.username_field = QLineEdit()
        self.username_field.setPlaceholderText("Username")
        self.username_field.setFixedSize(500, 45)
        self.layout.addWidget(self.username_field)

        # E-mail mező
        self.email_field = QLineEdit()
        self.email_field.setPlaceholderText("Email")
        self.email_field.setFixedSize(500, 45)
        self.layout.addWidget(self.email_field)

        # Jelszó létrehozási mező
        self.password_field = PasswordLineEdit()
        self.password_field.setPlaceholderText("Create password")
        self.password_field.setEchoMode(QLineEdit.Password)
        self.password_field.setFixedSize(500, 45)
        self.layout.addWidget(self.password_field)

        # Jelszó megerősítési mező
        self.confirm_password_field = PasswordLineEdit()
        self.confirm_password_field.setPlaceholderText("Confirm password")
        self.confirm_password_field.setEchoMode(QLineEdit.Password)
        self.confirm_password_field.setFixedSize(500, 45)
        self.confirm_password_field.returnPressed.connect(self.register)
        self.layout.addWidget(self.confirm_password_field)

        # Regisztrációs gomb
        self.register_button = QPushButton('Sign up')
        self.register_button.setFixedSize(500, 55)
        self.register_button.clicked.connect(self.register)
        self.layout.addWidget(self.register_button)
        self.layout.addSpacing(30)

        # Már van fiók? Bejelentkezés link
        self.login_label = QLabel('Already have an account? <a href="signup">Login</a>', self)
        self.login_label.setAlignment(Qt.AlignCenter)
        self.login_label.linkActivated.connect(self.open_login)
        self.layout.addWidget(self.login_label)
        self.layout.addSpacing(30)

        # Üzenet címke
        self.message_label = QLabel(self)
        self.message_label.setStyleSheet("color: red;")
        self.message_label.setAlignment(Qt.AlignCenter)
        self.message_label.setFixedSize(500, 40)
        self.message_label.hide()
        self.layout.addWidget(self.message_label)

        self.layout.setSpacing(10)
        self.layout.addStretch()

        self.setLayout(self.layout)
        self.center_window()

    def open_login(self):
        if self.settings_window.isVisible():
            self.settings_window.hide()
        self.hide()
        self.login_window.show()

    def register(self):
        username = self.username_field.text()
        email = self.email_field.text()
        password = self.password_field.text()
        confirm_password = self.confirm_password_field.text()

        if not loginUtils.is_valid_email(email):
            self.message_label.setText("Invalid email address!")
            self.message_label.show()
            return

        if not loginUtils.is_strong_password(password):
            self.message_label.setText("Too weak password!")
            self.message_label.show()
            return

        if password != confirm_password:
            self.message_label.setText("Password missmatch!")
            self.message_label.show()
            return

        if self.db_manager.user_exists(username, email):
            self.message_label.setText("Username or email address is already used!")
            self.message_label.show()
            return

        hashed_password = loginUtils.hash_password(password)

        if self.db_manager.add_user(username, email, hashed_password):
            self.username_field.setText('')
            self.email_field.setText('')
            self.password_field.setText('')
            self.confirm_password_field.setText('')
            self.message_label.hide()
            self.close()
            self.login_window.username_field.setText('')
            self.login_window.username_field.setFocus()
            self.login_window.setWindowModality(Qt.ApplicationModal)
            self.login_window.show()
            self.login_window.message_label.setStyleSheet("color: green;")
            self.login_window.message_label.setText("Registration successful!")
            self.login_window.message_label.show()
        else:
            self.message_label.setText("An error occurred during registration.\nPlease try again!")
            self.message_label.show()

    def setFontSize(self, size):
        font = self.font()
        font.setPointSize(size)
        self.username_field.setFont(font)
        self.email_field.setFont(font)
        self.password_field.setFont(font)
        self.confirm_password_field.setFont(font)
        self.register_button.setFont(font)
        self.message_label.setFont(font)
        self.login_label.setFont(font)
