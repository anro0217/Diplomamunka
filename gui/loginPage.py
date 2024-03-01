from PyQt5.QtCore import Qt, QSize
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QLineEdit, QPushButton, QVBoxLayout, QHBoxLayout, QLabel, QCheckBox, QApplication
from basePage import FramelessPage
from database.database import DatabaseManager
from gui.settingsPage import SettingsWindow
from resources import loginUtils
from resources.globalSignals import globalSignals


class LoginWindow(FramelessPage):
    def __init__(self, registration_window=None, main_window=None):
        super().__init__()
        self.registration_window = registration_window
        self.main_window = main_window
        globalSignals.fontSizeChanged.connect(self.setFontSize)
        globalSignals.themeChanged.connect(self.setTheme)
        self.initUI()
        self.setFontSize(20)

    def initUI(self):
        self.layout = QVBoxLayout(self)

        self.username_field = QLineEdit(self)
        self.username_field.setPlaceholderText("Username")
        #self.username_field.setStyleSheet("padding: 15px; border: none;")

        self.password_field = QLineEdit(self)
        self.password_field.setPlaceholderText("Password")
        self.password_field.setEchoMode(QLineEdit.Password)
        self.password_field.returnPressed.connect(self.open_main_window)
        #self.password_field.setStyleSheet("padding: 15px; border: none;")

        self.loginButton = QPushButton("Login", self)
        self.loginButton.clicked.connect(self.open_main_window)

        self.remember_me_checkbox = QCheckBox("Remember me", self)

        self.register_label = QLabel("Don't have an account? <a href='Sign up'>Sign up</a>", self)
        self.register_label.setAlignment(Qt.AlignCenter)
        self.register_label.setStyleSheet('margin-top: 10px;')
        self.register_label.linkActivated.connect(self.open_registration)

        self.exitButton = QPushButton("Exit", self)
        self.exitButton.clicked.connect(QApplication.instance().quit)

        # Hozzáadás sorrendjének beállítása
        self.layout.addWidget(self.username_field)
        self.layout.addWidget(self.password_field)
        self.layout.addWidget(self.remember_me_checkbox)  # Ezt ide helyezzük
        self.layout.addWidget(self.loginButton)
        self.layout.addWidget(self.register_label)

        # Alsó gombok elrendezése
        button_layout = QHBoxLayout()
        button_layout.addWidget(self.exitButton, alignment=Qt.AlignLeft)
        button_layout.addStretch()
        self.layout.addLayout(button_layout)

        self.center_window()

    def open_registration(self):
        self.hide()
        self.registration_window.show()

    def open_main_window(self):
        db_manager = DatabaseManager('database/application.db')
        username_or_email = self.username_field.text()
        password = self.password_field.text()
        if db_manager.validate_login(username_or_email, password):
            if self.remember_me_checkbox.isChecked():
                # Tárold el a felhasználói adatokat
                self.save_login_state(username_or_email)
            self.main_window.set_user_label(username_or_email)
            print("A bejelentkezés sikeres")
            self.close()
        else:
            print("Invalid username or password!")

    def save_login_state(self, username_or_email):
        with open('login_state.cfg', 'w') as f:
            f.write(username_or_email)

    def setTheme(self, darkModeEnabled):
        if darkModeEnabled:
            self.setStyleSheet("background-color: #333333; color: #ffffff;")
            self.settingsButton.setIcon(QIcon("resources/images/settings_light_icon.png"))
        else:
            self.setStyleSheet("background-color: #ffffff; color: #000000;")
            self.settingsButton.setIcon(QIcon("resources/images/settings_dark_icon.png"))

    def setFontSize(self, size):
        font = self.font()
        font.setPointSize(size)
        self.username_field.setFont(font)
        self.password_field.setFont(font)
        self.loginButton.setFont(font)
        #self.settingsButton.setIconSize(QSize(size * 2, size * 2))
        self.exitButton.setFont(font)
