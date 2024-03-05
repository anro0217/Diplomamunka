import os

from PyQt5.QtCore import Qt, QSize
from PyQt5.QtGui import QPixmap, QIcon
from PyQt5.QtWidgets import QWidget, QHBoxLayout, QVBoxLayout, QComboBox, QTextEdit, QPushButton, QPlainTextEdit, \
    QApplication, QLabel, QMenu, QAction, QListWidget, QSplitter, QGraphicsBlurEffect, QLineEdit
from baseWindow import FramelessWindow
from database.database import DatabaseManager
from gui.settingsPage import SettingsWindow
from resources import loginUtils
from resources.codeEditor import CodeEditor
from resources.databaseViewer import DatabaseViewer
from resources.globalSignals import globalSignals


class AdminWindow(FramelessWindow):
    def __init__(self, login_window):
        super().__init__(login_window)
        globalSignals.fontSizeChanged.connect(self.setFontSize)
        globalSignals.themeChanged.connect(self.setTheme)
        self.initUI()
        self.setFontSize(20)

    def initUI(self):

        # Lessons menu toggle gomb
        self.lessons_button = QPushButton()
        self.lessons_button.setIcon(QIcon('resources/images/menu_icon.png'))
        self.lessons_button.setFixedSize(45, 45)
        self.lessons_button.clicked.connect(self.toggle_lessons_dropdown)

        # Létrehozunk egy QListWidget-et a leckéknek
        self.lessons_list_widget = QListWidget()
        self.lessons_list_widget.addItems(["Hello World!", "Variables", "Lists"])
        self.lessons_list_widget.setMaximumWidth(200)  # Szélesség korlátozása
        self.lessons_list_widget.setVisible(False)  # Alapértelmezetten nem látható

        self.user_label = QLabel("")
        self.user_label.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        self.user_label.setDisabled(False)

        # Felhasználói menü/profile gomb
        self.user_menu_button = QPushButton()
        self.profile_icon = QIcon('resources/images/blank_profile.png')
        self.user_menu_button.setIcon(self.profile_icon)
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
        self.profile_action = QAction("Profile", self)
        self.settings_action = QAction("Settings", self)
        # settings_action.triggered.connect(self.open_settings_window)
        self.sign_out_action = QAction("Sign Out", self)
        self.sign_out_action.triggered.connect(self.sign_out)

        self.user_menu.addActions([self.settings_action, self.sign_out_action, self.profile_action])

        self.title_input = QLineEdit()
        self.title_input.setAlignment(Qt.AlignCenter)
        self.title_input.setFixedSize(300, 30)

        self.solution_input = QTextEdit()
        self.solution_input.setMaximumHeight(100)

        db_manager = DatabaseManager('database/application.db')
        self.database_viewer = DatabaseViewer(db_manager)

        self.task_input = QTextEdit()

        self.save_button = QPushButton(QIcon('resources/images/run_button.png'), "", self)
        self.save_button.setIconSize(QSize(50, 100))  # Az ikon méretének beállítása
        self.save_button.setFixedSize(55, 100)  # A gomb méretének beállítása
        self.save_button.setStyleSheet("text-align: left; padding: 5px;")
        self.save_button.clicked.connect(self.save_task)

        # Robot kép létrehozása
        self.robot_label = QLabel(self)
        self.robot_label.setPixmap(
            QPixmap('resources/images/robot.png'))
        self.robot_label.setFixedSize(215, 350)

        # A gombra és a label-re kerülő layout
        user_layout = QHBoxLayout()
        user_layout.addWidget(self.lessons_button)
        user_layout.addStretch()
        user_layout.addWidget(self.title_input, 1)
        user_layout.addStretch()
        user_layout.addWidget(self.user_label)
        user_layout.addWidget(self.user_menu_button)
        user_layout.setContentsMargins(0, 0, 10, 0)

        code_layout = QHBoxLayout()
        code_layout.addWidget(self.database_viewer, 2)
        code_layout.addWidget(self.task_input, 1)

        output_layout = QHBoxLayout()
        output_layout.addWidget(self.save_button)
        output_layout.addWidget(self.solution_input)

        lessons_layout = QVBoxLayout()
        lessons_layout.addWidget(self.robot_label, 0, Qt.AlignBottom)
        lessons_layout.addWidget(self.lessons_list_widget)

        # Create the top thin layout with a color
        top_layout_widget = QWidget()
        top_layout_widget.setFixedHeight(40)  # Adjust the height as needed
        top_layout_widget.setLayout(user_layout)

        # Create the left layout with a color
        left_layout_widget = QWidget()
        left_layout_widget.setFixedWidth(220)  # Adjust the width as needed
        left_layout_widget.setLayout(lessons_layout)

        # Create the top right layout with a color
        top_right_layout_widget = QWidget()
        top_right_layout_widget.setLayout(code_layout)

        # Create the bottom right layout with a color
        bottom_right_layout_widget = QWidget()
        bottom_right_layout_widget.setFixedHeight(120)  # Adjust the height as needed
        bottom_right_layout_widget.setLayout(output_layout)

        # Create the central horizontal layout which will contain left and right vertical layouts
        central_h_layout = QHBoxLayout()

        # Create the right layout which will be split into top and bottom layouts
        right_v_layout = QVBoxLayout()

        # Add the top and bottom right layouts to the right vertical layout
        right_v_layout.addWidget(top_right_layout_widget, 1)  # The 1 here makes the layout expandable
        right_v_layout.addWidget(bottom_right_layout_widget)

        # Add the left and right layouts to the central horizontal layout
        central_h_layout.addWidget(left_layout_widget)
        central_h_layout.addLayout(right_v_layout, 1)

        # Create the main vertical layout and add the top and central layouts
        main_v_layout = QVBoxLayout()
        main_v_layout.addWidget(top_layout_widget)
        main_v_layout.addLayout(central_h_layout, 1)

        # Set the layout of the central widget
        central_widget = QWidget()
        central_widget.setLayout(main_v_layout)
        self.setCentralWidget(central_widget)

        self.center_window()

    def save_task(self):
        db_manager = DatabaseManager('database/application.db')
        title = self.title_input.text()
        task = self.task_input.toPlainText()
        solution = self.solution_input.toPlainText()
        if title and task and solution:
            # Itt hozzáadhatjuk az adatokat az adatbázis táblához
            db_manager.add_task(title, task, solution)
        else:
            print("Minden mező kitöltése kötelező!")

    def setFontSize(self, size):
        # Set font size for the code editor and the output window
        # font = self.code_editor.font()
        # font.setPointSize(size)
        # self.code_editor.setFont(font)
        # self.output_window.setFont(font)
        pass

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
