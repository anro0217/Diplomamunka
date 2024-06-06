from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QLineEdit, QPushButton, QVBoxLayout, QHBoxLayout, QLabel, QCheckBox, QApplication
from basePage import FramelessPage
from gui.adminPage import AdminWindow
from gui.registrationPage import RegistrationWindow
from gui.userPage import UserWindow
from resources.utils import loginUtils
from resources.utils.globalSignals import globalSignals
from resources.widgets.myPasswordField import PasswordLineEdit


class LoginWindow(FramelessPage):
    def __init__(self):
        super().__init__()
        globalSignals.fontSizeChanged.connect(self.setFontSize)
        globalSignals.themeChanged.connect(self.setTheme)
        self.user_window = None
        self.admin_window = None
        self.registration_window = RegistrationWindow(self)
        self.setWindowModality(Qt.ApplicationModal)
        self.show()
        self.initUI()
        self.setFontSize(20)
        self.check_auto_login()

    def initUI(self):
        self.layout = QVBoxLayout(self)

        self.username_field = QLineEdit(self)
        self.username_field.setPlaceholderText("Username|Email")
        self.username_field.setFixedSize(500, 45)

        self.password_field = PasswordLineEdit()
        self.password_field.setPlaceholderText("Password")
        self.password_field.setEchoMode(QLineEdit.Password)
        self.password_field.setFixedSize(500, 45)
        self.password_field.returnPressed.connect(self.which_user)

        self.checkBox = QCheckBox("Remember me", self)
        self.checkBox.setFocusPolicy(Qt.StrongFocus)
        self.checkBox.setFixedSize(500, 30)
        self.checkBox.setStyleSheet("""
                    QCheckBox:focus {
                        border: none;
                        outline: none;
                    }""")

        self.loginButton = QPushButton("Login", self)
        self.loginButton.setFixedSize(500, 50)
        self.loginButton.clicked.connect(self.which_user)

        self.register_label = QLabel("Don't have an account? <a href='Sign up'>Sign up</a>", self)
        self.register_label.setAlignment(Qt.AlignCenter)
        self.register_label.setFixedSize(500, 20)
        self.register_label.linkActivated.connect(self.open_registration)

        self.message_label = QLabel(self)
        self.message_label.setStyleSheet("color: red;")
        self.message_label.setAlignment(Qt.AlignCenter)
        self.message_label.setFixedSize(500, 40)
        self.message_label.hide()

        self.exitButton = QPushButton("Exit", self)
        self.exitButton.setFixedSize(150, 50)
        self.exitButton.clicked.connect(QApplication.instance().quit)

        # Adding widgets to the layout in the desired order
        self.layout.addWidget(self.username_field)
        self.layout.addWidget(self.password_field)
        self.layout.addWidget(self.checkBox)
        self.layout.addWidget(self.loginButton)
        self.layout.addWidget(self.register_label)
        self.layout.addWidget(self.message_label)  # This is now below the register_label
        self.layout.setSpacing(10)
        self.layout.addStretch()  # This will push the exit button to the bottom

        # Bottom buttons layout
        button_layout = QHBoxLayout()
        button_layout.addWidget(self.exitButton, alignment=Qt.AlignLeft)
        button_layout.addStretch()
        self.layout.addLayout(button_layout)

        # Set tab order explicitly
        self.setTabOrder(self.username_field, self.password_field)
        self.setTabOrder(self.password_field, self.checkBox)
        self.setTabOrder(self.checkBox, self.loginButton)
        self.setTabOrder(self.loginButton, self.exitButton)

        self.setLayout(self.layout)
        self.center_window()

    def check_auto_login(self):
        try:
            with open('login_state.cfg', 'r', encoding='utf-8') as f:
                username = f.read().strip()
                if username and '\u200B' in username:
                    username = username.replace('\u200B', '')
                    user_id = self.db_manager.get_user_id_by_username_or_email(username)
                    self.create_windows(user_id, username == 'admin')
                    if username == 'admin':
                        self.admin_window.set_user_label(username)
                        self.admin_window.show()
                    else:
                        self.user_window.set_user_label(username)
                        self.user_window.show()
                    self.hide()
        except FileNotFoundError:
            pass

    def open_registration(self):
        self.message_label.hide()
        self.hide()
        self.registration_window.username_field.setText('')
        self.registration_window.email_field.setText('')
        self.registration_window.password_field.setText('')
        self.registration_window.confirm_password_field.setText('')
        self.registration_window.username_field.setFocus()
        self.registration_window.message_label.hide()
        self.registration_window.setWindowModality(Qt.ApplicationModal)
        self.registration_window.show()

    def which_user(self):
        username_or_email = self.username_field.text()
        password = self.password_field.text()
        if self.checkBox.isChecked():
            loginUtils.save_login_state(username_or_email)
        if username_or_email == 'admin':
            self.login_as_admin(username_or_email, password)
        else:
            self.login_as_user(username_or_email, password)

    def login_as_user(self, username_or_email, password):
        if self.db_manager.validate_login(username_or_email, password):
            self.open_user_window(username_or_email)
            self.message_label.hide()
            self.hide()
        else:
            self.message_label.setText("Invalid username or password!")
            self.message_label.setStyleSheet("color: red;")
            self.message_label.show()

    def open_user_window(self, username_or_email):
        user_id = self.db_manager.get_user_id_by_username_or_email(username_or_email)
        self.create_windows(user_id, False)
        self.user_window.set_user_label(username_or_email)
        self.user_window.show()

    def login_as_admin(self, username_or_email, password):
        if password == "admin_password":
            self.create_windows(None, True)
            self.admin_window.set_user_label(username_or_email)
            self.admin_window.show()
            self.message_label.hide()
            self.hide()
        else:
            self.message_label.setText("Invalid username or password!")
            self.message_label.setStyleSheet("color: red;")
            self.message_label.show()

    def open_admin_window(self, username_or_email):
        self.admin_window = AdminWindow(self, self.user_window)
        self.user_window = UserWindow(self, is_admin=True, admin_window=self.admin_window)
        self.admin_window.set_user_label(username_or_email)
        self.admin_window.show()

    def create_windows(self, user_id, is_admin):
        if self.admin_window is None:
            self.admin_window = AdminWindow(self, None)
        if self.user_window is None:
            self.user_window = UserWindow(self, user_id, is_admin, self.admin_window)
        self.admin_window.user_window = self.user_window
        self.user_window.admin_window = self.admin_window
        self.user_window.is_admin = is_admin
        self.user_window.user_id = user_id

    def setFontSize(self, size):
        font = self.font()
        font.setPointSize(size)
        self.username_field.setFont(font)
        self.password_field.setFont(font)
        self.loginButton.setFont(font)
        self.exitButton.setFont(font)
