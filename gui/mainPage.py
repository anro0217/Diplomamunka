import os
import sys
from contextlib import redirect_stdout
from io import StringIO

from PyQt5.QtCore import Qt, QSize
from PyQt5.QtGui import QPixmap, QIcon
from PyQt5.QtWidgets import QWidget, QHBoxLayout, QVBoxLayout, QComboBox, QTextEdit, QPushButton, QPlainTextEdit, \
    QApplication, QLabel, QMenu, QAction, QListWidget, QSplitter
from baseWindow import FramelessWindow
from gui.loginPage import LoginWindow
from gui.registrationPage import RegistrationWindow
from gui.settingsPage import SettingsWindow
from resources.codeEditor import CodeEditor
from resources.globalSignals import globalSignals


class MainWindow(FramelessWindow):
    def __init__(self, parent=None):
        super().__init__()
        globalSignals.fontSizeChanged.connect(self.setFontSize)
        globalSignals.themeChanged.connect(self.setTheme)
        self.initUI()
        self.check_auto_login()
        self.setFontSize(20)

    def initUI(self):

        self.placeholder_widget = QWidget()
        self.placeholder_widget.setFixedWidth(200)

        # Létrehozunk egy QListWidget-et a leckéknek
        self.lessons_list_widget = QListWidget()
        self.lessons_list_widget.addItems(["Hello World!", "Variables", "Lists"])
        self.lessons_list_widget.setMaximumWidth(200)  # Szélesség korlátozása
        self.lessons_list_widget.setVisible(False)  # Alapértelmezetten nem látható

        # Lessons menu toggle gomb
        self.lessons_button = QPushButton()
        self.lessons_button.setIcon(QIcon('resources/images/menu_icon.png'))
        self.lessons_button.clicked.connect(self.toggle_lessons_dropdown)

        # A lecke címe
        lesson_title = QLabel("TITLE OF THE LESSON")
        lesson_title.setAlignment(Qt.AlignCenter)

        # Felhasználónév vagy 'Sign In' felirat
        self.user_label = QLabel("Sign In")
        self.user_label.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        self.user_label.mousePressEvent = self.open_login_window
        self.user_label.setDisabled(False)

        # Felhasználói menü/profile gomb
        self.user_menu_button = QPushButton()
        profile_icon = QIcon('resources/images/blank_profile.png')
        self.user_menu_button.setIcon(profile_icon)
        self.user_menu_button.setIconSize(QSize(40, 40))  # Az ikon méretének beállítása
        self.user_menu_button.setFlat(True)
        self.user_menu_button.setFixedSize(40, 40)  # A gomb méretének beállítása
        self.user_menu_button.setStyleSheet(
            "QPushButton {"
            "border: none;"  # Eltávolítjuk a gomb keretét
            "border-radius: 20px;"  # Kör alakúra állítjuk
            "}"
            "QPushButton:pressed {"
            "border: 1px solid #8f8f91;"  # Megnyomáskor keretet adunk hozzá
            "}"
        )

        # Felhasználói menü létrehozása
        self.user_menu = QMenu()
        self.user_menu_button.setMenu(self.user_menu)
        profile_action = QAction("Profile", self)
        settings_action = QAction("Settings", self)
        settings_action.triggered.connect(self.open_settings_window)
        sign_out_action = QAction("Sign Out", self)
        sign_out_action.triggered.connect(self.sign_out)

        self.user_menu.addActions([settings_action, sign_out_action, profile_action])

        # Kód szerkesztő és kimeneti ablak
        self.code_editor = CodeEditor()
        self.output_window = QPlainTextEdit()
        self.output_window.setReadOnly(True)
        self.output_window.setMaximumHeight(100)

        # "Run CODE" gomb
        self.run_button = QPushButton("Run Code")
        self.run_button.clicked.connect(self.run_code)

        # Feladat leírás szövegdoboz
        self.task_description = QTextEdit()
        self.task_description.setReadOnly(True)

        # A gombra és a label-re kerülő layout
        user_layout = QHBoxLayout()
        user_layout.addWidget(self.user_label)
        user_layout.addWidget(self.user_menu_button)
        user_layout.setContentsMargins(0, 0, 10, 0)  # Beállítjuk a belső margót

        # Felső layout
        top_layout = QHBoxLayout()
        top_layout.addWidget(self.lessons_button)
        top_layout.addWidget(lesson_title, 1)
        top_layout.addWidget(self.user_menu_button)
        top_layout.addLayout(user_layout)  # A felhasználói layout hozzáadása

        # Központi layout
        central_layout = QHBoxLayout()
        central_layout.addWidget(self.lessons_list_widget)  # Hozzáadjuk a leckék listáját
        central_layout.addWidget(self.placeholder_widget)
        central_layout.addWidget(self.code_editor, 5)
        central_layout.addWidget(self.task_description, 2)

        # Alsó layout
        bottom_layout = QHBoxLayout()
        bottom_layout.addWidget(self.run_button)
        bottom_layout.addWidget(self.output_window, 5)

        # Fő layout
        main_layout = QVBoxLayout()
        main_layout.addLayout(top_layout)
        main_layout.addLayout(central_layout)
        main_layout.addLayout(bottom_layout)

        # Központi widget beállítása
        central_widget = QWidget()
        central_widget.setLayout(main_layout)
        self.setCentralWidget(central_widget)

        self.center_window()

    def toggle_lessons_dropdown(self):
        # Az üres helyet tartó widget és a leckék listájának láthatóságának váltogatása
        self.lessons_list_widget.setVisible(not self.lessons_list_widget.isVisible())
        self.placeholder_widget.setVisible(not self.lessons_list_widget.isVisible())

    def run_code(self):
        output_text = self.code_editor.run_code_and_capture_output()
        self.output_window.setPlainText(output_text)

    def open_login_window(self, event=None):
        # Létrehozzuk a bejelentkezési ablakot, ha még nem létezik
        if not hasattr(self, 'login_window'):
            self.login_window = LoginWindow(main_window=self)
        if not hasattr(self, 'registration_window'):
            self.registration_window = RegistrationWindow()
        self.login_window.registration_window = self.registration_window
        self.registration_window.login_window = self.login_window
        self.login_window.setWindowModality(Qt.ApplicationModal) #modális ablak, vagyis a többi blockolva amíg aktív
        self.login_window.show()

    def open_settings_window(self):
        # Létrehozzuk a beállítások ablakot, ha még nem létezik
        if not hasattr(self, 'settings_window'):
            self.settings_window = SettingsWindow(self)
        self.settings_window.show()


    def check_auto_login(self):
        try:
            with open('login_state.cfg', 'r') as f:
                username_or_email = f.read().strip()
                if username_or_email:
                    self.set_user_label(username_or_email)
                else:
                    self.open_login_window()
        except FileNotFoundError:
            self.open_login_window()

    def set_user_label(self,username):
        self.user_label.setText(username)
        self.user_label.setDisabled(True)

    def sign_out(self):
        if hasattr(self, 'login_window'):
            self.login_window.password_field.setText('')
            self.login_window.remember_me_checkbox.setChecked(False)
            self.login_window.setWindowModality(Qt.ApplicationModal)
            self.login_window.show()
        else:
            self.login_window = LoginWindow(main_window=self)
            with open('login_state.cfg', 'r') as f:
                self.login_window.username_field.setText(f.read().strip())
            self.login_window.password_field.setFocus()
            self.login_window.setWindowModality(Qt.ApplicationModal)
            self.login_window.show()
        self.delete_login_state()
        self.user_label.setText("Sign In")
        self.user_label.setDisabled(False)

        # Itt adhatod meg, hogy mi történjen még kijelentkezéskor, pl. UI reset

    def delete_login_state(self):
        try:
            os.remove('login_state.cfg')
        except FileNotFoundError:
            pass  # Ha a fájl nem létezik, nincs mit törölni

        # További teendők, ha szükséges, pl. felhasználói felület frissítése

    def setFontSize(self, size):
        # Set font size for the code editor and the output window
        font = self.code_editor.font()
        font.setPointSize(size)
        self.code_editor.setFont(font)
        self.output_window.setFont(font)

    def setTheme(self, darkModeEnabled):
        # Toggle the theme between dark and light mode
        if darkModeEnabled:
            self.setStyleSheet("background-color: #333333; color: #ffffff;")
            self.code_editor.setStyleSheet("""QPlainTextEdit {
                                    background-color: #1e1e1e;
                                    color: #dcdcdc;
                                    }""")
            self.output_window.setStyleSheet("""QPlainTextEdit {
                                    background-color: #252526;
                                    color: #dcdcdc;
                                    }""")
            self.task_description.setStyleSheet("""QTextEdit {
                                    background-color: #252526;
                                    color: #dcdcdc;
                                    }""")
        else:
            self.setStyleSheet("background-color: #ffffff; color: #000000;")
            self.code_editor.setStyleSheet("")
            self.output_window.setStyleSheet("")
            self.task_description.setStyleSheet("")
