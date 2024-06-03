from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QPlainTextEdit, QPushButton, QMessageBox


class DebuggingTask(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.initUI()

    def initUI(self):
        layout = QVBoxLayout()

        self.code_editor = QPlainTextEdit()
        layout.addWidget(self.code_editor)

        self.submit_button = QPushButton("Beküldés")
        self.submit_button.clicked.connect(self.check_code)
        layout.addWidget(self.submit_button)

        self.setLayout(layout)

    def load_task(self, task_data):
        self.task_data = task_data
        self.code_editor.setPlainText(task_data['debugging_code'])

    def check_code(self):
        user_code = self.code_editor.toPlainText()
        correct_code = self.task_data['correct_code']

        if user_code.strip() == correct_code.strip():
            QMessageBox.information(self, "Correct", "Your solution is correct!")
        else:
            QMessageBox.warning(self, "Incorrect", "Your solution is incorrect.")

