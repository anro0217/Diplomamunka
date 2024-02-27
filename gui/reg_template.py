from PyQt5.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QHBoxLayout,
    QLineEdit, QPushButton, QLabel, QFrame
)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon, QPixmap


class RegistrationWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Regisztráció')
        self.setFixedSize(400, 600)  # Ablak méretének beállítása
        self.initUI()

    def initUI(self):
        layout = QVBoxLayout()

        # Fejléc
        header_label = QLabel('Signup', self)
        header_label.setAlignment(Qt.AlignCenter)
        header_label.setStyleSheet('font-size: 24px; font-weight: bold; margin-top: 20px;')
        layout.addWidget(header_label)

        # Felhasználónév mező
        self.username_field = QLineEdit()
        self.username_field.setPlaceholderText("Username")
        layout.addWidget(self.username_field)

        # E-mail mező
        self.email_field = QLineEdit()
        self.email_field.setPlaceholderText("Email")
        layout.addWidget(self.email_field)

        # Jelszó létrehozási mező
        self.password_field = QLineEdit()
        self.password_field.setPlaceholderText("Create password")
        self.password_field.setEchoMode(QLineEdit.Password)
        layout.addWidget(self.password_field)

        # Jelszó megerősítési mező
        self.confirm_password_field = QLineEdit()
        self.confirm_password_field.setPlaceholderText("Confirm password")
        self.confirm_password_field.setEchoMode(QLineEdit.Password)
        layout.addWidget(self.confirm_password_field)

        # Regisztrációs gomb
        self.register_button = QPushButton('Signup')
        self.register_button.setIcon(
            QIcon(QPixmap("path/to/lock_icon.png")))  # Cseréld ki a saját ikonod elérési útjára
        self.register_button.setStyleSheet('font-size: 16px;')
        layout.addWidget(self.register_button)

        # Már van fiók? Bejelentkezés link
        login_label = QLabel('Already have an account? <a href="#">Login</a>', self)
        login_label.setAlignment(Qt.AlignCenter)
        login_label.setStyleSheet('margin-top: 10px;')
        layout.addWidget(login_label)

        # Divider vonal
        divider = QFrame()
        divider.setFrameShape(QFrame.HLine)
        divider.setFrameShadow(QFrame.Sunken)
        layout.addWidget(divider)

        # Külső szolgáltatók gombjai
        social_layout = QHBoxLayout()
        # Facebook gomb stílusa és hozzáadása a QHBoxLayout-hoz
        facebook_button = QPushButton('Login with Facebook')
        facebook_button.setStyleSheet('font-size: 16px; background-color: #3b5998; color: white;')
        social_layout.addWidget(facebook_button)

        # Google gomb stílusa és hozzáadása a QHBoxLayout-hoz
        google_button = QPushButton(QIcon('path/to/google_icon.png'), 'Login with Google')
        google_button.setStyleSheet('font-size: 16px; background-color: #db4437; color: white;')
        social_layout.addWidget(google_button)

        # A közösségi gombokat tartalmazó layout hozzáadása a fő QVBoxLayout-hoz
        layout.addLayout(social_layout)

        # Eseménykezelők hozzárendelése
        self.register_button.clicked.connect(self.register)
        facebook_button.clicked.connect(self.login_facebook)
        google_button.clicked.connect(self.login_google)
        login_label.linkActivated.connect(self.open_login)

        # A widget beállításai
        self.setLayout(layout)

    def register(self):
        # Regisztráció eseménykezelő
        pass

    def login_facebook(self):
        # Facebook bejelentkezés eseménykezelő
        pass

    def login_google(self):
        # Google bejelentkezés eseménykezelő
        pass

    def open_login(self):
        # Bejelentkező oldal megnyitása
        pass

    # A QApplication létrehozása és az ablak megjelenítése
if __name__ == '__main__':
    app = QApplication([])
    win = RegistrationWindow()
    win.show()
    app.exec_()



