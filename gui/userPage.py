from PyQt5.QtCore import Qt, QSize, QPoint
from PyQt5.QtGui import QPixmap, QIcon, QFont
from PyQt5.QtWidgets import QWidget, QHBoxLayout, QVBoxLayout, QPushButton, QLabel, QMenu, QAction, QListWidget, \
    QApplication, QStackedWidget, QMessageBox, QListWidgetItem
from baseWindow import FramelessWindow
from resources.task_types.codeDebuggingTask import DebuggingTask
from resources.task_types.dragAndDropTask import DragAndDropTask
from resources.task_types.matchingTask import MatchingTask
from resources.task_types.quizTask import QuizTask
from resources.utils.globalSignals import globalSignals
from resources.widgets.speechBubble import SpeechBubble
from resources.task_types.codingTask import CodeRunner  # Import the TaskArea class


class UserWindow(FramelessWindow):
    def __init__(self, login_window, is_admin=False):
        super().__init__(login_window)
        globalSignals.fontSizeChanged.connect(self.setFontSize)
        globalSignals.themeChanged.connect(self.setTheme)
        self.admin_window = login_window
        self.is_admin = is_admin
        self.initUI()

    def showEvent(self, event):
        super().showEvent(event)
        self.lessons_list_widget.clear()
        tasks = self.db_manager.get_tasks()
        for task in tasks:
            item = QListWidgetItem(task['title'])
            item.setData(Qt.UserRole, task['id'])  # Store the unique id
            self.lessons_list_widget.addItem(item)

    def initUI(self):
        # Lessons menu toggle button
        self.lessons_button = QPushButton()
        self.lessons_button.setIcon(QIcon('resources/images/menu_icon.png'))
        self.lessons_button.setFixedSize(45, 45)
        self.lessons_button.setIconSize(QSize(40, 40))
        self.lessons_button.clicked.connect(self.toggle_lessons_dropdown)

        # Create a QListWidget for the lessons
        self.lessons_list_widget = QListWidget()
        self.lessons_list_widget.setMaximumWidth(200)
        self.lessons_list_widget.setVisible(False)
        self.lessons_list_widget.itemClicked.connect(self.on_lesson_clicked)

        # Lesson title
        self.lesson_title = QLabel("")
        self.lesson_title.setAlignment(Qt.AlignCenter)

        self.user_label = QLabel("")
        self.user_label.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        self.user_label.setDisabled(False)

        # User menu/profile button
        self.user_menu_button = QPushButton()
        self.profile_icon = QIcon('resources/images/blank_profile.png')
        self.user_menu_button.setIcon(self.profile_icon)
        self.user_menu_button.setIconSize(QSize(40, 40))
        self.user_menu_button.setFlat(True)
        self.user_menu_button.setFixedSize(40, 40)
        self.user_menu_button.setStyleSheet(
            "QPushButton {"
            "border: none;"
            "border-radius: 20px;"
            "}"
            "QPushButton:pressed {"
            "border: 1px solid #8f8f91;"
            "}"
        )

        # Create user menu
        self.user_menu = QMenu()
        self.user_menu_button.setMenu(self.user_menu)
        self.profile_action = QAction("Profile", self)
        self.settings_action = QAction("Settings", self)
        self.sign_out_action = QAction("Sign Out", self)
        self.sign_out_action.triggered.connect(self.sign_out)
        self.exit_action = QAction("Exit", self)
        self.exit_action.triggered.connect(QApplication.instance().quit)

        self.user_menu.addActions([self.settings_action, self.sign_out_action, self.profile_action, self.exit_action])

        # Create speech bubble for task description
        self.speech_bubble = SpeechBubble()

        # Robot image
        self.robot_label = QLabel(self)
        self.robot_label.setPixmap(QPixmap('resources/images/robot.png'))
        self.robot_label.setFixedSize(215, 350)
        self.robot_label.mousePressEvent = self.toggle_speech_bubble

        # Layout for the top row (lessons button, lesson title, user label, user menu button)
        user_layout = QHBoxLayout()
        user_layout.addWidget(self.lessons_button)
        user_layout.addWidget(self.lesson_title, 1)
        user_layout.addWidget(self.user_label)
        user_layout.addWidget(self.user_menu_button)
        user_layout.setContentsMargins(0, 0, 10, 0)

        lessons_layout = QVBoxLayout()
        lessons_layout.addWidget(self.robot_label, 0, Qt.AlignBottom)
        lessons_layout.addWidget(self.lessons_list_widget)

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
        self.empty_widget = QWidget()
        self.task_area.addWidget(self.empty_widget)
        self.code_runner = CodeRunner()
        self.task_area.addWidget(self.code_runner)
        self.drag_and_drop_task = DragAndDropTask()
        self.task_area.addWidget(self.drag_and_drop_task)
        self.matching_task = MatchingTask()
        self.task_area.addWidget(self.matching_task)
        self.quiz_task = QuizTask()
        self.task_area.addWidget(self.quiz_task)
        self.debugging_task = DebuggingTask()
        self.task_area.addWidget(self.debugging_task)

        # Initially show the empty widget
        self.task_area.setCurrentWidget(self.empty_widget)

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

        if self.is_admin:
            self.switch_to_admin_button.show()

        self.center_window()
        self.show_speech_bubble()
        self.setFontSize(10)

    def switch_to_admin_view(self):
        self.hide()
        self.admin_window.show()

    def show_speech_bubble(self):
        self.speech_bubble.move(self.robot_label.mapToGlobal(QPoint(220, -self.speech_bubble.height() // 2)))
        self.speech_bubble.show()

    def toggle_speech_bubble(self, event):
        if self.speech_bubble.isVisible():
            self.speech_bubble.hide()
        else:
            if len(self.speech_bubble.getText().strip()) != 0:
                self.show_speech_bubble()

    def on_lesson_clicked(self, item):
        task_id = item.data(Qt.UserRole)  # Retrieve the unique id
        task_data = self.db_manager.get_task_by_id(task_id)  # Fetch task data using the unique id
        if task_data:
            self.lesson_title.setText(task_data['title'])
            self.speech_bubble.setText(task_data['description'])
            self.toggle_lessons_dropdown()
            self.show_speech_bubble()

            task_type = task_data['type']
            if task_type == 'code':
                self.task_area.setCurrentWidget(self.code_runner)
                self.code_runner.load_task(task_data)
            elif task_type == 'drag_and_drop':
                self.task_area.setCurrentWidget(self.drag_and_drop_task)
                self.drag_and_drop_task.load_task(task_data)
            elif task_type == 'matching':
                self.task_area.setCurrentWidget(self.matching_task)
                self.matching_task.load_task(task_data)
            elif task_type == 'quiz':
                self.task_area.setCurrentWidget(self.quiz_task)
                self.quiz_task.load_task(task_data)
            elif task_type == 'debugging':
                self.task_area.setCurrentWidget(self.debugging_task)
                self.debugging_task.load_task(task_data)
            else:
                self.task_area.setCurrentWidget(self.empty_widget)
        else:
            QMessageBox.warning(self, "Hiba", "Nem sikerült betölteni a feladatot.")

    def setFontSize(self, size):
        self.lesson_title.setStyleSheet(f"font-size: {size}pt;")
        self.lessons_list_widget.setStyleSheet(f"font-size: {size}pt;")
        self.user_label.setStyleSheet(f"font-size: {size}pt;")
        self.user_menu_button.setStyleSheet(f"font-size: {size}pt;")
        self.lessons_button.setStyleSheet(f"font-size: {size}pt;")
        self.speech_bubble.setStyleSheet(f"font-size: {size}pt;")
        self.switch_to_admin_button.setStyleSheet(f"font-size: {size}pt;")
        self.task_area.setStyleSheet(f"font-size: {size}pt;")

    def setTheme(self, darkModeEnabled):
        if darkModeEnabled:
            self.setStyleSheet("background-color: #333333; color: #ffffff;")
        else:
            self.setStyleSheet("background-color: #ffffff; color: #000000;")
