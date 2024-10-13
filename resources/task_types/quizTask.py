from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QRadioButton, QPushButton, QButtonGroup, QMessageBox
import random

class QuizTask(QWidget):
    def __init__(self, db_manager, parent=None):
        super().__init__(parent)
        self.db_manager = db_manager
        self.parent_window = parent
        self.initUI()

    def initUI(self):
        self.layout = QVBoxLayout()

        self.question = QLabel("")
        self.layout.addWidget(self.question)

        self.button_group = QButtonGroup()
        self.option_buttons = []  # List to store the option buttons

        # Create a radio button for each possible option (up to 4)
        for _ in range(4):
            radio_button = QRadioButton()
            self.layout.addWidget(radio_button)
            self.button_group.addButton(radio_button)
            self.option_buttons.append(radio_button)

        self.layout.addStretch()

        # Add the submit button at the bottom
        self.submit_button = QPushButton("Check answer")
        self.submit_button.clicked.connect(self.check_answer)
        self.layout.addWidget(self.submit_button)

        self.setLayout(self.layout)

    def load_task(self, task_data, user_id):
        self.task_data = task_data
        self.user_id = user_id
        self.question.setText(task_data['quiz_question'])
        options = task_data['quiz_options'].split('\n')

        # Clear previous options
        for button in self.option_buttons:
            button.setVisible(False)

        # Shuffle options
        random.shuffle(options)

        # Set the options to the radio buttons based on the number of options
        for i in range(len(options)):
            if i < len(self.option_buttons):  # Limit to the number of radio buttons
                self.option_buttons[i].setText(options[i])
                self.option_buttons[i].setVisible(True)

        # Hide the radio buttons if there are fewer options
        for j in range(len(options), len(self.option_buttons)):
            self.option_buttons[j].setVisible(False)

    def check_answer(self):
        selected_button = self.button_group.checkedButton()
        if selected_button:
            user_answer = selected_button.text()
            correct_answer = self.task_data['quiz_answer']
            if user_answer == correct_answer:
                QMessageBox.information(self, "Correct", "Your answer is correct!")
                if self.parent_window and not self.parent_window.is_admin:
                    self.db_manager.mark_task_as_completed(self.user_id, self.task_data['id'])
                    self.parent_window.update_lessons_list()
                    self.parent_window.get_next_task(self.task_data['id'])
            else:
                QMessageBox.warning(self, "Incorrect", "Your answer is incorrect.")
                if self.parent_window and not self.parent_window.is_admin:
                    self.db_manager.increment_failure_count(self.user_id, self.task_data['id'])
        else:
            QMessageBox.warning(self, "No Selection", "Please select an option.")
