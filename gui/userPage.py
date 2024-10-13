from PyQt5.QtCore import Qt, QSize, QPoint
from PyQt5.QtGui import QPixmap, QIcon, QFont, QColor, QFontMetrics
from PyQt5.QtWidgets import QWidget, QHBoxLayout, QVBoxLayout, QPushButton, QLabel, QMenu, QAction, QListWidget, \
    QApplication, QStackedWidget, QMessageBox, QListWidgetItem, QDialog
from baseWindow import FramelessWindow
from resources.task_types.codeDebuggingTask import DebuggingTask
from resources.task_types.dragAndDropTask import DragAndDropTask
from resources.task_types.matchingTask import MatchingTask
from resources.task_types.materialPage import MaterialPage
from resources.task_types.quizTask import QuizTask
from resources.task_types.statisticsPage import StatisticsPage
from resources.task_types.welcomePage import WelcomePage
from resources.utils.globalSignals import globalSignals
from resources.widgets.speechBubble import SpeechBubble
from resources.task_types.codingTask import CodeRunner


class UserWindow(FramelessWindow):
    def __init__(self, login_window, user_id=None, is_admin=False, admin_window=None):
        super().__init__(login_window)
        self.admin_window = admin_window
        self.is_admin = is_admin
        self.user_id = user_id
        self.current_widget = None
        self.initUI()
        globalSignals.fontSizeChanged.connect(self.setFontSize)
        globalSignals.themeChanged.connect(self.setTheme)
        self.load_user_settings()

    def initUI(self):
        # Lessons menu toggle button
        self.lessons_button = QPushButton()
        self.lessons_button.setIcon(QIcon('resources/images/menu_icon.png'))
        self.lessons_button.setFixedSize(45, 45)
        self.lessons_button.setIconSize(QSize(40, 40))
        self.lessons_button.clicked.connect(self.toggle_lessons_dropdown)

        self.lessons_text = QLabel("Lessons")

        # Create a QListWidget for the lessons
        self.lessons_list_widget = QListWidget()
        self.lessons_list_widget.setMaximumWidth(200)
        self.lessons_list_widget.setVisible(False)
        self.lessons_list_widget.itemClicked.connect(self.on_lesson_clicked)

        self.statistics_button = QPushButton("Check statistics", self)
        self.statistics_button.setMaximumWidth(200)
        self.statistics_button.setVisible(False)
        self.statistics_button.clicked.connect(self.on_statistics_clicked)

        # Lesson title
        self.lesson_title = QLabel("")
        self.lesson_title.setAlignment(Qt.AlignCenter)

        self.user_label = QLabel("")
        self.user_label.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        self.user_label.setDisabled(False)

        # Create speech bubble for task description
        self.speech_bubble = SpeechBubble()

        # Robot image
        self.robot_label = QLabel(self)
        self.robot_label.setPixmap(QPixmap('resources/images/robot.png'))
        self.robot_label.setFixedSize(215, 350)
        self.robot_label.mousePressEvent = self.toggle_speech_bubble

        self.check_icon = QIcon('resources/images/check_icon.png')

        # Layout for the top row (lessons button, lesson title, user label, user menu button)
        user_layout = QHBoxLayout()
        user_layout.addWidget(self.lessons_button)
        user_layout.addWidget(self.lessons_text)
        user_layout.addWidget(self.lesson_title, 1)
        user_layout.addWidget(self.user_label)
        user_layout.addWidget(self.user_menu_button)
        user_layout.setContentsMargins(0, 0, 10, 0)

        lessons_layout = QVBoxLayout()
        lessons_layout.addWidget(self.robot_label, 0, Qt.AlignBottom)
        lessons_layout.addWidget(self.lessons_list_widget)
        lessons_layout.addWidget(self.statistics_button)

        # Create the top thin layout with a color
        top_layout_widget = QWidget()
        top_layout_widget.setFixedHeight(40)
        top_layout_widget.setLayout(user_layout)

        # Create the left layout with a color
        left_layout_widget = QWidget()
        left_layout_widget.setFixedWidth(220)
        left_layout_widget.setLayout(lessons_layout)

        # Task area
        self.task_area = QStackedWidget()

        self.welcome_page = WelcomePage(self)
        self.task_area.addWidget(self.welcome_page)

        self.material_page = MaterialPage(self)
        self.task_area.addWidget(self.material_page)

        self.statistics_page = StatisticsPage(self.db_manager, self.user_id, parent=self)
        self.task_area.addWidget(self.statistics_page)

        self.code_runner = CodeRunner(self.db_manager, parent=self)
        self.task_area.addWidget(self.code_runner)

        self.drag_and_drop_task = DragAndDropTask(self.db_manager, parent=self)
        self.task_area.addWidget(self.drag_and_drop_task)

        self.matching_task = MatchingTask(self.db_manager, parent=self)
        self.task_area.addWidget(self.matching_task)

        self.quiz_task = QuizTask(self.db_manager, parent=self)
        self.task_area.addWidget(self.quiz_task)

        self.debugging_task = DebuggingTask(self.db_manager, parent=self)
        self.task_area.addWidget(self.debugging_task)

        # Initially show the empty widget
        self.task_area.setCurrentWidget(self.welcome_page)

        # Create the right layout which will be split into top and bottom layouts
        right_v_layout = QVBoxLayout()
        right_v_layout.addWidget(self.task_area, 1)

        self.switch_to_admin_button = QPushButton("Switch to Admin View", self)
        self.switch_to_admin_button.clicked.connect(self.switch_to_admin_view)
        right_v_layout.addWidget(self.switch_to_admin_button)
        self.switch_to_admin_button.hide()

        # Create the central horizontal layout which will contain left and right vertical layouts
        central_h_layout = QHBoxLayout()
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

    def load_user_settings(self):
        settings = self.db_manager.load_user_settings(self.user_id)
        if settings:
            theme = settings.get('theme')
            font_size = settings.get('font_size')

            if font_size is not None:
                self.setFontSize(font_size)
            else:
                self.setFontSize(10)

            if theme is not None:
                self.setTheme(theme == 'dark')
            else:
                self.setTheme(False)

            self.settings_window.updateLayout(font_size, theme == 'dark')

    def showEvent(self, event):
        super().showEvent(event)
        self.load_user_settings()
        self.update_lessons_list()

        if self.is_admin:
            self.switch_to_admin_button.show()
        else:
            self.switch_to_admin_button.hide()

    def update_lessons_list(self):
        self.lessons_list_widget.clear()
        tasks = self.db_manager.get_tasks()
        completed_tasks = self.db_manager.get_completed_tasks(self.user_id)

        for task in tasks:
            item = QListWidgetItem(task['title'])
            item.setData(Qt.UserRole, task['id'])

            if task['id'] in completed_tasks:
                item.setFlags(item.flags() & ~Qt.ItemIsSelectable)
                item.setForeground(QColor('gray'))
                item.setIcon(self.check_icon)

            self.lessons_list_widget.addItem(item)

    def switch_to_admin_view(self):
        self.hide()
        self.admin_window.show()

    def show_speech_bubble(self):
        if self.task_area.currentWidget() != self.material_page:
            self.speech_bubble.move(self.robot_label.mapToGlobal(QPoint(220, -self.speech_bubble.height() // 2)))
            self.speech_bubble.show()

    def toggle_speech_bubble(self, event):
        if self.task_area.currentWidget() != self.material_page:
            if self.speech_bubble.isVisible():
                self.speech_bubble.hide()
            else:
                if len(self.speech_bubble.getText().strip()) != 0:
                    self.show_speech_bubble()

    def on_lesson_clicked(self, item):
        task_id = item.data(Qt.UserRole)
        task_data = self.db_manager.get_task_by_id(task_id)

        if task_data:
            self.lesson_title.setText(task_data['title'])
            self.speech_bubble.setText(task_data['description'])
            self.toggle_lessons_dropdown()

            if task_data.get('material'):
                self.task_area.setCurrentWidget(self.material_page)
                self.material_page.load_material(task_data['material'])
                self.material_page.set_start_task_callback(lambda: self.load_task_area(task_data))
                self.speech_bubble.hide()
            else:
                self.load_task_area(task_data)
        else:
            QMessageBox.warning(self, "Error", "Cannot load task")

    def on_statistics_clicked(self):
        self.current_widget = self.task_area.currentWidget()
        self.statistics_page.update_task_table()
        self.statistics_page.update_statistics()
        self.task_area.setCurrentWidget(self.statistics_page)
        self.toggle_lessons_dropdown()

    def on_close_statistics(self):
        if self.current_widget:
            self.task_area.setCurrentWidget(self.current_widget)
            self.toggle_lessons_dropdown()

    def load_task_area(self, task_data):
        task_type = task_data['type']
        if task_type == 'code':
            self.task_area.setCurrentWidget(self.code_runner)
            self.code_runner.load_task(task_data, self.user_id)
        elif task_type == 'drag & drop':
            self.task_area.setCurrentWidget(self.drag_and_drop_task)
            self.drag_and_drop_task.load_task(task_data, self.user_id)
        elif task_type == 'matching':
            self.task_area.setCurrentWidget(self.matching_task)
            self.matching_task.load_task(task_data, self.user_id)
        elif task_type == 'quiz':
            self.task_area.setCurrentWidget(self.quiz_task)
            self.quiz_task.load_task(task_data, self.user_id)
        elif task_type == 'debugging':
            self.task_area.setCurrentWidget(self.debugging_task)
            self.debugging_task.load_task(task_data, self.user_id)
        else:
            self.task_area.setCurrentWidget(self.welcome_page)
        self.show_speech_bubble()

    def get_next_task(self, current_task_id):
        tasks = self.db_manager.get_tasks()
        completed_tasks = self.db_manager.get_completed_tasks(self.user_id)
        current_task_index = next((index for (index, task) in enumerate(tasks) if task['id'] == current_task_id), -1)

        # Ha az aktuális feladatot megtaláltuk és van következő feladat
        if current_task_index != -1:
            # Iterálunk a következő feladatok között
            for task in tasks[current_task_index + 1:]:
                if task['id'] not in completed_tasks:
                    task_data = self.db_manager.get_task_by_id(task['id'])
                    self.lesson_title.setText(task_data['title'])
                    self.speech_bubble.setText(task_data['description'])

                    if task_data.get('material'):
                        self.task_area.setCurrentWidget(self.material_page)
                        self.material_page.load_material(task_data['material'])
                        self.material_page.set_start_task_callback(lambda: self.load_task_area(task_data))
                        self.speech_bubble.hide()
                    else:
                        self.load_task_area(task_data)
                    return
        if False: #TODO: Ez csak akkor jöjjön fel, ha tényleg mindegyik kész!
            QMessageBox.information(self, "Done", "You have completed all tasks!")

    def setFontSize(self, size):
        self.font_size = size
        self.update_user_menu_style()

        self.lessons_text.setStyleSheet(f"font-size: {size}pt;")
        self.lesson_title.setStyleSheet(f"font-size: {size}pt;")
        self.lessons_list_widget.setStyleSheet(f"font-size: {size}pt;")
        self.user_label.setStyleSheet(f"font-size: {size}pt;")
        self.user_menu_button.setStyleSheet(f"font-size: {size}pt;")
        self.lessons_button.setStyleSheet(f"font-size: {size}pt;")
        if size <= 17:
            self.statistics_button.setStyleSheet(f"font-size: {size}pt;")
        else:
            self.statistics_button.setStyleSheet(f"font-size: {17}pt;")
        self.speech_bubble.setStyleSheet(f"font-size: {size}pt;")
        self.switch_to_admin_button.setStyleSheet(f"font-size: {size}pt;")
        self.task_area.setStyleSheet(f"font-size: {size}pt;")
        self.statistics_page.set_font_size(size)
        self.code_runner.set_font_size(size)

        if self.user_id is not None:
            self.db_manager.save_user_settings(self.user_id, None, size)

    def setTheme(self, darkModeEnabled):
        self.dark_mode_enabled = darkModeEnabled
        self.update_user_menu_style()

        if darkModeEnabled:
            theme = 'dark'
            self.setStyleSheet("background-color: #333333; color: #ffffff;")
            self.check_icon = QIcon('resources/images/check_icon_light.png')
            self.lessons_button.setIcon(QIcon('resources/images/menu_icon_light.png'))
        else:
            theme = 'light'
            self.setStyleSheet("background-color: #ffffff; color: #000000;")
            self.check_icon = QIcon('resources/images/check_icon.png')
            self.lessons_button.setIcon(QIcon('resources/images/menu_icon.png'))

        self.code_runner.set_theme(darkModeEnabled)
        self.statistics_page.set_theme(darkModeEnabled)
        self.speech_bubble.updateTheme(darkModeEnabled)

        if self.user_id is not None:
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
