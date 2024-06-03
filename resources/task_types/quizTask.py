from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QRadioButton, QPushButton, QButtonGroup, QMessageBox


class QuizTask(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.initUI()

    def initUI(self):
        self.layout = QVBoxLayout()

        self.question = QLabel("")
        self.layout.addWidget(self.question)

        self.button_group = QButtonGroup()
        self.option_buttons = []

        for _ in range(4):
            radio_button = QRadioButton()
            self.layout.addWidget(radio_button)
            self.button_group.addButton(radio_button)
            self.option_buttons.append(radio_button)

        self.submit_button = QPushButton("Beküldés")
        self.submit_button.clicked.connect(self.check_answer)
        self.layout.addWidget(self.submit_button)

        self.setLayout(self.layout)

    def load_task(self, task_data):
        self.task_data = task_data
        self.question.setText(task_data['quiz_question'])
        options = task_data['quiz_options'].split('\n')
        for i, option in enumerate(options):
            self.option_buttons[i].setText(option)

    def check_answer(self):
        selected_button = self.button_group.checkedButton()
        if selected_button:
            user_answer = selected_button.text()
            correct_answer = self.task_data['quiz_answer']
            if user_answer == correct_answer:
                QMessageBox.information(self, "Correct", "Your answer is correct!")
            else:
                QMessageBox.warning(self, "Incorrect", "Your answer is incorrect.")
        else:
            QMessageBox.warning(self, "No Selection", "Please select an option.")

