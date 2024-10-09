from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QPlainTextEdit, QPushButton, QMessageBox


class DebuggingTask(QWidget):
    def __init__(self, db_manager, parent=None):
        super().__init__(parent)
        self.db_manager = db_manager
        self.parent_window = parent
        self.initUI()

    def initUI(self):
        layout = QVBoxLayout()

        self.code_editor = QPlainTextEdit()
        layout.addWidget(self.code_editor)

        self.submit_button = QPushButton("Check code")
        self.submit_button.clicked.connect(self.check_code)
        layout.addWidget(self.submit_button)

        self.setLayout(layout)

    def load_task(self, task_data, user_id):
        self.task_data = task_data
        self.user_id = user_id
        self.code_editor.setPlainText(task_data['debugging_code'])

    def check_code(self):
        user_code = self.code_editor.toPlainText()
        correct_code = self.task_data['correct_code']

        if user_code.strip() == correct_code.strip():
            QMessageBox.information(self, "Correct", "Your solution is correct!")
            if self.parent_window and not self.parent_window.is_admin:
                self.db_manager.mark_task_as_completed(self.user_id, self.task_data['id'])
                self.parent_window.update_lessons_list()
                self.parent_window.get_next_task(self.task_data['id'])
        else:
            QMessageBox.warning(self, "Incorrect", "Your solution is incorrect.")
            if self.parent_window and not self.parent_window.is_admin:
                self.db_manager.increment_failure_count(self.user_id, self.task_data['id'])

