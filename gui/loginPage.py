from PyQt5.QtCore import Qt, QPropertyAnimation, QRect
from PyQt5.QtWidgets import QLineEdit, QPushButton, QLabel, QVBoxLayout, QHBoxLayout, QDialog, QFrame, QWidget
from gui.basePage import FramelessWindow
from gui.settingsPage import SettingsPage
from gui.resources.globalSignals import globalSignals


class LoginPage(FramelessWindow):
    def __init__(self):
        super().__init__()
        globalSignals.fontSizeChanged.connect(self.setFontSize)
        globalSignals.themeChanged.connect(self.setTheme)
        self.initUI()

    def initUI(self):
        self.username_field = QLineEdit(self)
        self.username_field.setPlaceholderText("Username")
        self.username_field.setStyleSheet("padding: 15px; border: none;")

        self.password_field = QLineEdit(self)
        self.password_field.setPlaceholderText("Password")
        self.password_field.setEchoMode(QLineEdit.Password)
        self.password_field.setStyleSheet("padding: 15px; border: none;")

        self.loginButton = QPushButton("Login", self)
        self.registerButton = QPushButton("Register", self)
        self.settingsButton = QPushButton("Settings", self)
        self.exitButton = QPushButton("Exit", self)

        self.layout = QVBoxLayout(self)
        self.layout.addWidget(self.username_field)
        self.layout.addWidget(self.password_field)
        self.layout.addWidget(self.loginButton)
        self.layout.addWidget(self.registerButton)
        self.layout.addWidget(self.settingsButton)
        self.layout.addWidget(self.exitButton)

        # Alsó gombok elrendezése
        button_layout = QHBoxLayout()
        button_layout.addWidget(self.exitButton, alignment=Qt.AlignLeft)
        button_layout.addStretch()
        button_layout.addWidget(self.settingsButton, alignment=Qt.AlignRight)
        self.layout.addLayout(button_layout)

        # Beállítások panel példányosítása
        self.settingsPage = SettingsPage(self)

        # Gomb eseménykezelője
        self.settingsButton.clicked.connect(self.toggleSettingsPanel)
        self.exitButton.clicked.connect(self.close)

        self.center_window()

    def toggleSettingsPanel(self):
        self.settingsPage.toggleVisibility(self.geometry())

    def setTheme(self, darkModeEnabled):
        if darkModeEnabled:
            self.setStyleSheet("background-color: #333333; color: #ffffff;")
        else:
            self.setStyleSheet("background-color: #ffffff; color: #000000;")

    def setFontSize(self, size):
        font = self.font()
        font.setPointSize(size)
        self.username_field.setFont(font)
        self.password_field.setFont(font)
        self.loginButton.setFont(font)
        self.registerButton.setFont(font)
        self.settingsButton.setFont(font)
        self.exitButton.setFont(font)


