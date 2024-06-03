from PyQt5.QtCore import Qt, QSize
from PyQt5.QtGui import QPixmap, QIcon, QFont
from PyQt5.QtWidgets import QWidget, QHBoxLayout, QVBoxLayout, QTextEdit, QPushButton, \
    QApplication, QLabel, QMenu, QAction, QListWidget, QLineEdit, QMessageBox, QComboBox, QFormLayout, QSpacerItem, \
    QSizePolicy, QToolButton
from baseWindow import FramelessWindow
from resources.widgets.databaseViewer import DatabaseViewer
from resources.utils.globalSignals import globalSignals
from gui.userPage import UserWindow


class AdminWindow(FramelessWindow):
    def __init__(self, login_window):
        super().__init__(login_window)
        globalSignals.fontSizeChanged.connect(self.setFontSize)
        globalSignals.themeChanged.connect(self.setTheme)
        self.user_window = UserWindow(self, True)
        self.initUI()

    def initUI(self):
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
        self.sign_out_action = QAction("Sign Out", self)
        self.sign_out_action.triggered.connect(self.sign_out)
        self.exit_action = QAction("Exit", self)
        self.exit_action.triggered.connect(QApplication.instance().quit)

        self.user_menu.addActions([self.settings_action, self.sign_out_action, self.profile_action, self.exit_action])

        # Feladat mezők létrehozása
        self.title_input = QLineEdit()
        self.title_input.setAlignment(Qt.AlignCenter)
        self.title_input.setFixedSize(300, 30)
        self.title_input.setPlaceholderText("Enter the task title here")

        self.description_input = QTextEdit()
        self.description_input.setMaximumHeight(100)
        self.description_input.setPlaceholderText("Enter the task description here")
        self.add_help_icon(self.description_input, "Mező formátuma: ")

        self.task_type_selector = QComboBox()
        self.task_type_selector.addItems(["code", "drag_and_drop", "matching", "quiz", "debugging"])
        self.task_type_selector.currentIndexChanged.connect(self.update_task_fields)
        self.task_type_selector.setFixedWidth(300)

        self.code_template_input = QTextEdit()
        self.code_template_input.setMaximumHeight(100)
        self.code_template_input.setPlaceholderText("Enter the code template here")
        self.add_help_icon(self.code_template_input, "Mező formátuma: ")

        self.code_result_input = QTextEdit()
        self.code_result_input.setMaximumHeight(100)
        self.code_result_input.setPlaceholderText("Enter the code result here")
        self.add_help_icon(self.code_result_input, "Mező formátuma: ")

        self.drag_drop_input = QTextEdit()
        self.drag_drop_input.setMaximumHeight(100)
        self.drag_drop_input.setPlaceholderText("Enter drag & drop items here")
        self.add_help_icon(self.drag_drop_input, "Mező formátuma: ")

        self.matching_input = QTextEdit()
        self.matching_input.setMaximumHeight(100)
        self.matching_input.setPlaceholderText("Enter matching pairs here")
        self.add_help_icon(self.matching_input, "Mező formátuma: ")

        self.quiz_question_input = QTextEdit()
        self.quiz_question_input.setMaximumHeight(100)
        self.quiz_question_input.setPlaceholderText("Enter the quiz question here")
        self.add_help_icon(self.quiz_question_input, "Mező formátuma: ")

        self.quiz_options_input = QTextEdit()
        self.quiz_options_input.setMaximumHeight(100)
        self.quiz_options_input.setPlaceholderText("Enter the quiz options here")
        self.add_help_icon(self.quiz_options_input, "Mező formátuma: ")

        self.quiz_answer_input = QTextEdit()
        self.quiz_answer_input.setMaximumHeight(100)
        self.quiz_answer_input.setPlaceholderText("Enter the quiz answer here")
        self.add_help_icon(self.quiz_answer_input, "Mező formátuma: ")

        self.debugging_code_input = QTextEdit()
        self.debugging_code_input.setMaximumHeight(100)
        self.debugging_code_input.setPlaceholderText("Enter the debugging code here")
        self.add_help_icon(self.debugging_code_input, "Mező formátuma: ")

        self.correct_code_input = QTextEdit()
        self.correct_code_input.setMaximumHeight(100)
        self.correct_code_input.setPlaceholderText("Enter the correct code here")
        self.add_help_icon(self.correct_code_input, "Mező formátuma: ")

        self.form_layout = QVBoxLayout()
        self.form_layout.addWidget(self.task_type_selector)
        self.form_layout.addWidget(self.description_input)
        self.form_layout.addWidget(self.code_template_input)
        self.form_layout.addWidget(self.code_result_input)
        self.form_layout.addWidget(self.drag_drop_input)
        self.form_layout.addWidget(self.matching_input)
        self.form_layout.addWidget(self.quiz_question_input)
        self.form_layout.addWidget(self.quiz_options_input)
        self.form_layout.addWidget(self.quiz_answer_input)
        self.form_layout.addWidget(self.debugging_code_input)
        self.form_layout.addWidget(self.correct_code_input)

        self.task_fields_widget = QWidget()
        self.task_fields_widget.setLayout(self.form_layout)

        self.database_viewer = DatabaseViewer(self.db_manager)

        self.save_button = QPushButton(QIcon('resources/images/run_button.png'), "", self)
        self.save_button.setIconSize(QSize(55, 60))  # Az ikon méretének beállítása
        self.save_button.setFixedSize(55, 50)  # A gomb méretének beállítása
        self.save_button.clicked.connect(self.save_task)

        self.delete_button = QPushButton(QIcon('resources/images/delete_button.png'), "", self)
        self.delete_button.setIconSize(QSize(40, 40))  # Ikon méretének beállítása
        self.delete_button.setFixedSize(55, 50)  # Gomb méretének beállítása
        self.delete_button.clicked.connect(self.delete_task)

        # Robot kép létrehozása
        self.robot_label = QLabel(self)
        self.robot_label.setPixmap(QPixmap('resources/images/robot.png'))
        self.robot_label.setFixedSize(215, 350)

        # A gombra és a label-re kerülő layout
        user_layout = QHBoxLayout()
        user_layout.addStretch()
        user_layout.addWidget(self.title_input, 1)
        user_layout.addStretch()
        user_layout.addWidget(self.user_label)
        user_layout.addWidget(self.user_menu_button)
        user_layout.setContentsMargins(0, 0, 10, 0)

        # A feladattípus választó és leírás mező elrendezése
        fixed_layout = QVBoxLayout()
        fixed_layout.addWidget(self.task_type_selector)
        fixed_layout.addWidget(self.description_input)

        task_layout = QVBoxLayout()
        task_layout.addLayout(fixed_layout)
        task_layout.addWidget(self.task_fields_widget)

        # A gombok elrendezése a task mezők alatt
        buttons_layout = QHBoxLayout()
        buttons_layout.addWidget(self.save_button)
        buttons_layout.addWidget(self.delete_button)

        # Jobb oldali layout (task mezők és gombok)
        right_layout = QVBoxLayout()
        right_layout.addLayout(task_layout)
        right_layout.addLayout(buttons_layout)

        code_layout = QHBoxLayout()
        code_layout.addWidget(self.database_viewer, 2)
        code_layout.addLayout(right_layout, 1)

        lessons_layout = QVBoxLayout()
        lessons_layout.addWidget(self.robot_label, 0, Qt.AlignBottom)
        # lessons_layout.addWidget(self.lessons_list_widget)

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

        # Create the central horizontal layout which will contain left and right vertical layouts
        central_h_layout = QHBoxLayout()

        # Create the right layout which will be split into top and bottom layouts
        right_v_layout = QVBoxLayout()

        # Add the top and bottom right layouts to the right vertical layout
        right_v_layout.addWidget(top_right_layout_widget, 1)  # The 1 here makes the layout expandable

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

        # Kezdetben csak a feladattípus mezőket frissítjük
        self.update_task_fields()

        # Add the switch button for user view
        self.switch_to_user_button = QPushButton("Switch to User View", self)
        self.switch_to_user_button.clicked.connect(self.switch_to_user_view)
        buttons_layout.addWidget(self.switch_to_user_button)

        self.setFontSize(10)

    def update_task_fields(self):
        task_type = self.task_type_selector.currentText()
        self.code_template_input.setVisible(task_type == "code")
        self.code_result_input.setVisible(task_type == "code")
        self.drag_drop_input.setVisible(task_type == "drag_and_drop")
        self.matching_input.setVisible(task_type == "matching")
        self.quiz_question_input.setVisible(task_type == "quiz")
        self.quiz_options_input.setVisible(task_type == "quiz")
        self.quiz_answer_input.setVisible(task_type == "quiz")
        self.debugging_code_input.setVisible(task_type == "debugging")
        self.correct_code_input.setVisible(task_type == "debugging")

    def add_help_icon(self, widget, help_text):
        layout = QHBoxLayout(widget)
        widget.setLayout(layout)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.addWidget(widget, 1)
        help_button = QToolButton()
        help_button.setIcon(QIcon('resources/images/help_icon.png'))
        help_button.setIconSize(QSize(16, 16))
        help_button.setStyleSheet("border: none;")
        help_button.setToolTip(help_text)
        layout.addWidget(help_button, 0, Qt.AlignBottom | Qt.AlignRight)

    def save_task(self):
        title = self.title_input.text().strip()
        description = self.description_input.toPlainText().strip()
        task_type = self.task_type_selector.currentText()
        code_template = self.code_template_input.toPlainText().strip() if task_type == "code" else None
        code_result = self.code_result_input.toPlainText().strip() if task_type == "code" else None
        drag_drop_items = self.drag_drop_input.toPlainText().strip() if task_type == "drag_and_drop" else None
        matching_pairs = self.matching_input.toPlainText().strip() if task_type == "matching" else None
        quiz_question = self.quiz_question_input.toPlainText().strip() if task_type == "quiz" else None
        quiz_options = self.quiz_options_input.toPlainText().strip() if task_type == "quiz" else None
        quiz_answer = self.quiz_answer_input.toPlainText().strip() if task_type == "quiz" else None
        debugging_code = self.debugging_code_input.toPlainText().strip() if task_type == "debugging" else None
        correct_code = self.correct_code_input.toPlainText().strip() if task_type == "debugging" else None

        required_fields = [title, description]
        if task_type == "code":
            required_fields.extend([code_template, code_result])
        elif task_type == "drag_and_drop":
            required_fields.append(drag_drop_items)
        elif task_type == "matching":
            required_fields.append(matching_pairs)
        elif task_type == "quiz":
            required_fields.extend([quiz_question, quiz_options, quiz_answer])
        elif task_type == "debugging":
            required_fields.extend([debugging_code, correct_code])

        if all(required_fields):
            self.db_manager.add_task(
                title, description, task_type, code_template, code_result, drag_drop_items,
                matching_pairs, quiz_question, quiz_options, quiz_answer, debugging_code, correct_code
            )
            self.database_viewer.load_table_data(self.database_viewer.table_selector.currentIndex())
        else:
            QMessageBox.warning(self, "Hiányzó mezők", "Minden mező kitöltése kötelező!")

    def delete_task(self):
        selected_record_id = self.database_viewer.get_selected_record_id()
        if selected_record_id is not None:
            # Megerősítő párbeszédablak létrehozása
            reply = QMessageBox.question(self, 'Rekord törlése',
                                         'Biztosan törölni szeretnéd ezt a rekordot?',
                                         QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
            # Csak akkor töröljük a rekordot, ha az admin az Igen-t választja
            if reply == QMessageBox.Yes:
                table_name = self.database_viewer.table_selector.currentText()
                self.db_manager.delete(table_name, selected_record_id)
                self.database_viewer.load_table_data(self.database_viewer.table_selector.currentIndex())
        else:
            print("No record is selected for deletion.")

    def setFontSize(self, size):
        self.title_input.setStyleSheet(f"font-size: {size}pt;")
        self.description_input.setStyleSheet(f"font-size: {size}pt;")
        self.task_type_selector.setStyleSheet(f"font-size: {size}pt;")
        self.code_template_input.setStyleSheet(f"font-size: {size}pt;")
        self.code_result_input.setStyleSheet(f"font-size: {size}pt;")
        self.drag_drop_input.setStyleSheet(f"font-size: {size}pt;")
        self.matching_input.setStyleSheet(f"font-size: {size}pt;")
        self.quiz_question_input.setStyleSheet(f"font-size: {size}pt;")
        self.quiz_options_input.setStyleSheet(f"font-size: {size}pt;")
        self.quiz_answer_input.setStyleSheet(f"font-size: {size}pt;")
        self.debugging_code_input.setStyleSheet(f"font-size: {size}pt;")
        self.correct_code_input.setStyleSheet(f"font-size: {size}pt;")
        self.user_label.setStyleSheet(f"font-size: {size}pt;")
        self.user_menu_button.setStyleSheet(f"font-size: {size}pt;")
        self.switch_to_user_button.setStyleSheet(f"font-size: {size}pt;")
        self.save_button.setStyleSheet(f"font-size: {size}pt;")
        self.delete_button.setStyleSheet(f"font-size: {size}pt;")

    def setTheme(self, darkModeEnabled):
        if darkModeEnabled:
            self.setStyleSheet("background-color: #333333; color: #ffffff;")
        else:
            self.setStyleSheet("background-color: #ffffff; color: #000000;")

    def switch_to_user_view(self):
        self.hide()
        self.user_window.show()

    def switch_to_admin_view(self):
        self.user_window.hide()
        self.show()
