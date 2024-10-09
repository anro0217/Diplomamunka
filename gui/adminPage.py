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
    def __init__(self, login_window, user_window):
        super().__init__(login_window)
        self.user_window = user_window
        self.user_id = 0
        self.initUI()
        globalSignals.fontSizeChanged.connect(self.setFontSize)
        globalSignals.themeChanged.connect(self.setTheme)
        self.load_user_settings()

    def initUI(self):
        self.user_label = QLabel("")
        self.user_label.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        self.user_label.setDisabled(False)

        # Feladat mezők létrehozása
        self.title_input = QTextEdit()
        self.title_input.setFixedWidth(300)
        self.title_input.setPlaceholderText("Enter the task title here")
        self.title_input.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.title_input.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)

        self.description_input = QTextEdit()
        self.description_input.setMaximumHeight(100)
        self.description_input.setPlaceholderText("Enter the task description here")
        self.add_help_icon(self.description_input, "Field format: ")

        self.task_type_selector = QComboBox()
        self.task_type_selector.addItems(["code", "drag_and_drop", "matching", "quiz", "debugging"])
        self.task_type_selector.currentIndexChanged.connect(self.update_task_fields)
        self.task_type_selector.setFixedWidth(300)

        self.code_template_input = QTextEdit()
        self.code_template_input.setMaximumHeight(100)
        self.code_template_input.setPlaceholderText("Enter the code template here")
        self.add_help_icon(self.code_template_input, "Field format: ")

        self.code_result_input = QTextEdit()
        self.code_result_input.setMaximumHeight(100)
        self.code_result_input.setPlaceholderText("Enter the code result here")
        self.add_help_icon(self.code_result_input, "Field format: ")

        self.drag_drop_input = QTextEdit()
        self.drag_drop_input.setMaximumHeight(100)
        self.drag_drop_input.setPlaceholderText("Enter drag & drop items here")
        self.add_help_icon(self.drag_drop_input, "Field format: ")

        self.matching_input = QTextEdit()
        self.matching_input.setMaximumHeight(100)
        self.matching_input.setPlaceholderText("Enter matching pairs here")
        self.add_help_icon(self.matching_input, "Field format: ")

        self.quiz_question_input = QTextEdit()
        self.quiz_question_input.setMaximumHeight(100)
        self.quiz_question_input.setPlaceholderText("Enter the quiz question here")
        self.add_help_icon(self.quiz_question_input, "Field format: ")

        self.quiz_options_input = QTextEdit()
        self.quiz_options_input.setMaximumHeight(100)
        self.quiz_options_input.setPlaceholderText("Enter the quiz options here")
        self.add_help_icon(self.quiz_options_input, "Field format: ")

        self.quiz_answer_input = QTextEdit()
        self.quiz_answer_input.setMaximumHeight(100)
        self.quiz_answer_input.setPlaceholderText("Enter the quiz answer here")
        self.add_help_icon(self.quiz_answer_input, "Field format: ")

        self.debugging_code_input = QTextEdit()
        self.debugging_code_input.setMaximumHeight(100)
        self.debugging_code_input.setPlaceholderText("Enter the debugging code here")
        self.add_help_icon(self.debugging_code_input, "Field format: ")

        self.correct_code_input = QTextEdit()
        self.correct_code_input.setMaximumHeight(100)
        self.correct_code_input.setPlaceholderText("Enter the correct code here")
        self.add_help_icon(self.correct_code_input, "Field format: ")

        # Tananyag szövegmező létrehozása, kezdetben elrejtve
        self.material_input = QTextEdit()
        self.material_input.setPlaceholderText("Write here the metarial for the lesson")
        self.material_input.setVisible(False)  # Kezdetben rejtve

        # Gomb a tananyag mező megnyitásához/becsukásához
        self.material_button = QPushButton("Show Material")
        self.material_button.setCheckable(True)
        self.material_button.setChecked(False)
        self.material_button.clicked.connect(self.toggle_material_input)

        self.form_layout = QVBoxLayout()
        self.form_layout.addWidget(self.task_type_selector)
        self.form_layout.addWidget(self.material_button)
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

        self.database_viewer = DatabaseViewer(self.db_manager, self.user_id)
        self.database_viewer.table_selector.currentIndexChanged.connect(self.toggle_edit_button)

        self.save_button = QPushButton(QIcon('resources/images/run_button.png'), "", self)
        self.save_button.setIconSize(QSize(55, 60))  # Az ikon méretének beállítása
        self.save_button.setFixedSize(55, 50)  # A gomb méretének beállítása
        self.save_button.clicked.connect(self.save_task)

        self.delete_button = QPushButton(QIcon('resources/images/delete_button.png'), "", self)
        self.delete_button.setIconSize(QSize(40, 40))  # Ikon méretének beállítása
        self.delete_button.setFixedSize(55, 50)  # Gomb méretének beállítása
        self.delete_button.clicked.connect(self.delete_task)

        self.edit_button = QPushButton(QIcon('resources/images/edit.png'), "", self)
        self.edit_button.setIconSize(QSize(40, 40))
        self.edit_button.setFixedSize(55, 50)
        self.edit_button.clicked.connect(self.edit_task)

        # Add the switch button for user view
        self.switch_to_user_button = QPushButton("Switch to User View", self)
        self.switch_to_user_button.clicked.connect(self.switch_to_user_view)

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
        fixed_layout.addWidget(self.material_button)
        fixed_layout.addWidget(self.description_input)

        task_layout = QVBoxLayout()
        task_layout.addLayout(fixed_layout)
        task_layout.addWidget(self.task_fields_widget)

        # A gombok elrendezése a task mezők alatt
        buttons_layout = QHBoxLayout()
        buttons_layout.addWidget(self.save_button)
        buttons_layout.addWidget(self.delete_button)
        buttons_layout.addWidget(self.edit_button)
        buttons_layout.addWidget(self.switch_to_user_button)

        # Jobb oldali layout (task mezők és gombok)
        right_layout = QVBoxLayout()
        right_layout.addLayout(task_layout)
        right_layout.addLayout(buttons_layout)

        code_layout = QHBoxLayout()
        code_layout.addWidget(self.database_viewer, 2)
        code_layout.addWidget(self.material_input, 2)
        code_layout.addLayout(right_layout, 1)

        lessons_layout = QVBoxLayout()
        lessons_layout.addWidget(self.robot_label, 0, Qt.AlignBottom)
        # lessons_layout.addWidget(self.lessons_list_widget)

        # Create the top thin layout with a color
        top_layout_widget = QWidget()
        top_layout_widget.setFixedHeight(50)  # Adjust the height as needed
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
        self.update_task_fields()
        self.setFocus()

    def showEvent(self, event):
        self.load_user_settings()

    def load_user_settings(self):
        settings = self.db_manager.load_user_settings(self.user_id)
        if settings:
            theme = settings.get('theme')
            font_size = settings.get('font_size')
            isDarkMode = theme == 'dark'

            if font_size is not None:
                self.setFontSize(font_size)
            else:
                self.setFontSize(10)

            if theme is not None:
                self.setTheme(isDarkMode)
            else:
                self.setTheme(False)

            self.settings_window.updateLayout(font_size, isDarkMode)

    def toggle_material_input(self):
        if self.material_button.isChecked():
            self.material_input.setVisible(True)
            self.database_viewer.setVisible(False)  # Az adatbázis nézet elrejtése
            self.material_button.setText("Hide Material")
        else:
            self.material_input.setVisible(False)
            self.database_viewer.setVisible(True)  # Az adatbázis nézet újra látható
            self.material_button.setText("Show Material")

    def toggle_edit_button(self):
        table_name = self.database_viewer.table_selector.currentText()
        # Ha a kiválasztott tábla nem "tasks", akkor a gomb legyen letiltva és elhomályosítva
        if table_name == "tasks":
            self.edit_button.setEnabled(True)
        else:
            self.edit_button.setEnabled(False)

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
        title = self.title_input.toPlainText().strip()
        description = self.description_input.toPlainText().strip()
        task_type = self.task_type_selector.currentText()
        material = self.material_input.toPlainText().strip()
        code_template = self.code_template_input.toPlainText().strip() if task_type == "code" else None
        code_result = self.code_result_input.toPlainText().strip() if task_type == "code" else None
        drag_drop_items = self.drag_drop_input.toPlainText().strip() if task_type == "drag_and_drop" else None
        matching_pairs = self.matching_input.toPlainText().strip() if task_type == "matching" else None
        quiz_question = self.quiz_question_input.toPlainText().strip() if task_type == "quiz" else None
        quiz_options = self.quiz_options_input.toPlainText().strip() if task_type == "quiz" else None
        quiz_answer = self.quiz_answer_input.toPlainText().strip() if task_type == "quiz" else None
        debugging_code = self.debugging_code_input.toPlainText().strip() if task_type == "debugging" else None
        correct_code = self.correct_code_input.toPlainText().strip() if task_type == "debugging" else None

        required_fields = [title, material, description]
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
            selected_record_id = self.database_viewer.get_selected_record_id()
            if selected_record_id is not None:
                # Frissítjük a meglévő rekordot
                self.db_manager.update_task(
                    selected_record_id, title, description, task_type, code_template, code_result, drag_drop_items,
                    matching_pairs, quiz_question, quiz_options, quiz_answer, debugging_code, correct_code, material
                )
                self.clear_cells()
            else:
                # Ellenőrizzük, hogy létezik-e már rekord ezzel a címmel
                existing_task = self.db_manager.get_task_by_title(title)
                if existing_task is None:
                    # Új rekord hozzáadása
                    self.db_manager.add_task(
                        title, description, task_type, code_template, code_result, drag_drop_items,
                        matching_pairs, quiz_question, quiz_options, quiz_answer, debugging_code, correct_code, material
                    )
                    self.clear_cells()
                else:
                    QMessageBox.warning(self, "Rekord létezik", "A rekord már létezik ezzel a címmel.")

            self.database_viewer.load_table_data(self.database_viewer.table_selector.currentIndex())
        else:
            QMessageBox.warning(self, "Hiányzó mezők", "Minden mező kitöltése kötelező!")

    def clear_cells(self):
        self.title_input.clear()
        self.description_input.clear()
        self.material_input.clear()
        self.code_template_input.clear()
        self.code_result_input.clear()
        self.drag_drop_input.clear()
        self.matching_input.clear()
        self.quiz_question_input.clear()
        self.quiz_options_input.clear()
        self.quiz_answer_input.clear()
        self.debugging_code_input.clear()
        self.correct_code_input.clear()
        self.database_viewer.setVisible(True)
        self.material_button.setChecked(False)
        self.material_input.setVisible(False)

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

    def edit_task(self):
        selected_record_id = self.database_viewer.get_selected_record_id()
        if selected_record_id is not None:
            # Kiválasztott rekord adatai
            record = self.db_manager.get_task_by_id(selected_record_id)

            # A rekord adataival való mezőkitöltés
            self.title_input.setText(record['title'])
            self.description_input.setPlainText(record['description'])
            self.task_type_selector.setCurrentText(record['type'])
            self.material_input.setPlainText(record['material'])

            # Típus alapú mezők frissítése
            self.update_task_fields()

            if record['type'] == 'code':
                self.code_template_input.setPlainText(record['code_template'])
                self.code_result_input.setPlainText(record['code_result'])
            elif record['type'] == 'drag_and_drop':
                self.drag_drop_input.setPlainText(record['drag_drop_items'])
            elif record['type'] == 'matching':
                self.matching_input.setPlainText(record['matching_pairs'])
            elif record['type'] == 'quiz':
                self.quiz_question_input.setPlainText(record['quiz_question'])
                self.quiz_options_input.setPlainText(record['quiz_options'])
                self.quiz_answer_input.setPlainText(record['quiz_answer'])
            elif record['type'] == 'debugging':
                self.debugging_code_input.setPlainText(record['debugging_code'])
                self.correct_code_input.setPlainText(record['correct_code'])

            # Any additional setup required for editing can go here

        else:
            QMessageBox.warning(self, "Nincs kiválasztott rekord", "Kérlek válassz ki egy rekordot a szerkesztéshez.")

    def setFontSize(self, size):
        self.font_size = size
        self.update_user_menu_style()

        font = QFont()
        font.setPointSize(size)

        self.title_input.setFont(font)
        self.description_input.setFont(font)
        self.code_template_input.setFont(font)
        self.code_result_input.setFont(font)
        self.drag_drop_input.setFont(font)
        self.matching_input.setFont(font)
        self.quiz_question_input.setFont(font)
        self.quiz_options_input.setFont(font)
        self.quiz_answer_input.setFont(font)
        self.debugging_code_input.setFont(font)
        self.correct_code_input.setFont(font)
        self.material_input.setFont(font)

        font_size_style = f"font-size: {size}pt;"

        for widget in [self.user_label, self.user_menu_button, self.switch_to_user_button,
                       self.save_button, self.delete_button,
                       self.material_button, self.task_type_selector]:
            current_style = widget.styleSheet()
            updated_style = f"{current_style} {font_size_style}"
            widget.setStyleSheet(updated_style)

        self.database_viewer.setFontSize(size)

        self.db_manager.save_user_settings(self.user_id, None, size)

    def setTheme(self, darkModeEnabled):
        self.dark_mode_enabled = darkModeEnabled
        self.update_user_menu_style()

        if darkModeEnabled:
            theme = 'dark'
            self.setStyleSheet("background-color: #333333; color: #ffffff;")
            self.edit_button.setIcon(QIcon('resources/images/edit_light.png'))

            # Külön beállítjuk a QTextEdit komponensekre is a sötét témát
            self.description_input.setStyleSheet("background-color: #333333; color: #ffffff;")
            self.code_template_input.setStyleSheet("background-color: #333333; color: #ffffff;")
            self.code_result_input.setStyleSheet("background-color: #333333; color: #ffffff;")

        else:
            theme = 'light'
            self.setStyleSheet("background-color: #ffffff; color: #000000;")
            self.edit_button.setIcon(QIcon('resources/images/edit.png'))

            # Visszaállítjuk a QTextEdit komponensek világos témáját
            self.description_input.setStyleSheet("background-color: #ffffff; color: #000000;")
            self.code_template_input.setStyleSheet("background-color: #ffffff; color: #000000;")
            self.code_result_input.setStyleSheet("background-color: #ffffff; color: #000000;")

        self.database_viewer.toggle_theme(darkModeEnabled)

        self.db_manager.save_user_settings(self.user_id, theme, None)

    def update_user_menu_style(self):
        # Generáljuk le a teljes stíluslapot a betűméret és a téma alapján
        font_size = getattr(self, 'font_size', 12)  # Alapértelmezett 12, ha nincs megadva
        dark_mode = getattr(self, 'dark_mode_enabled', False)

        if dark_mode:
            self.user_menu.setStyleSheet(
                f"QMenu {{"
                f"font-size: {font_size}pt;"
                "background-color: #2c2c2c;"
                "color: #ffffff;"
                "border: 1px solid #8f8f91;"
                "}}"
                "QMenu::item:selected {"
                "background-color: #3d3d3d;"
                "}"
            )
        else:
            self.user_menu.setStyleSheet(
                f"QMenu {{"
                f"font-size: {font_size}pt;"
                "background-color: #ffffff;"
                "color: #000000;"
                "border: 1px solid #cfcfcf;"
                "}}"
                "QMenu::item:selected {"
                "background-color: #f0f0f0;"
                "}"
            )

    def switch_to_user_view(self):
        self.hide()
        self.user_window.show()

    def switch_to_admin_view(self):
        self.user_window.hide()
        self.show()
