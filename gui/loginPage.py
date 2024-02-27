from PyQt5.QtCore import Qt, QSize
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QLineEdit, QPushButton, QVBoxLayout, QHBoxLayout, QLabel
from basePage import FramelessWindow
from gui.settingsPage import SettingsPage
from resources.globalSignals import globalSignals


class LoginPage(FramelessWindow):
    def __init__(self, registration_window=None):
        super().__init__()
        self.registration_window = registration_window
        globalSignals.fontSizeChanged.connect(self.setFontSize)
        globalSignals.themeChanged.connect(self.setTheme)
        self.initUI()
        self.setFontSize(10)

    def initUI(self):
        self.username_field = QLineEdit(self)
        self.username_field.setPlaceholderText("Username")
        #self.username_field.setStyleSheet("padding: 15px; border: none;")

        self.password_field = QLineEdit(self)
        self.password_field.setPlaceholderText("Password")
        self.password_field.setEchoMode(QLineEdit.Password)
        #self.password_field.setStyleSheet("padding: 15px; border: none;")

        self.loginButton = QPushButton("Login", self)


        self.register_label = QLabel('Don\'t have an account? <a href="signup">Sign up</a>', self)
        self.register_label.setAlignment(Qt.AlignCenter)
        self.register_label.setStyleSheet('margin-top: 10px;')
        self.register_label.linkActivated.connect(self.open_registration)


        self.settingsButton = QPushButton(self)
        self.settingsButton.setIcon(QIcon("resources/images/settings_dark_icon.png"))

        self.exitButton = QPushButton("Exit", self)

        self.layout = QVBoxLayout(self)
        self.layout.addWidget(self.username_field)
        self.layout.addWidget(self.password_field)
        self.layout.addWidget(self.loginButton)
        self.layout.addWidget(self.register_label)
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

    def open_registration(self):
        if self.settingsPage.isVisible():
            self.settingsPage.toggleVisibility(self.geometry())
        self.hide()
        self.registration_window.show()

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
        self.settingsButton.setIconSize(QSize(size * 2, size * 2))
        self.exitButton.setFont(font)



