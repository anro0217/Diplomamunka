import random
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QListWidget, QListWidgetItem, QMessageBox, QPushButton


class DragAndDropTask(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.initUI()

    def initUI(self):
        layout = QVBoxLayout()

        self.list_widget = QListWidget()
        layout.addWidget(self.list_widget)
        self.list_widget.setDragDropMode(QListWidget.InternalMove)

        self.check_button = QPushButton("Check Order", self)
        self.check_button.setFixedSize(100, 30)
        self.check_button.clicked.connect(self.check_order)
        layout.addWidget(self.check_button)

        self.setLayout(layout)

    def load_task(self, task_data):
        self.task_data = task_data
        self.list_widget.clear()
        items = task_data['drag_drop_items'].split('\n')
        self.correct_order = items[:]  # Tároljuk a helyes sorrendet

        # Keverjük össze az elemek sorrendjét
        random.shuffle(items)
        for item in items:
            list_item = QListWidgetItem(item)
            self.list_widget.addItem(list_item)

    def check_order(self):
        user_order = [self.list_widget.item(i).text() for i in range(self.list_widget.count())]

        if user_order == self.correct_order:
            QMessageBox.information(self, "Correct", "Your solution is correct!")
        else:
            QMessageBox.warning(self, "Incorrect", "Your solution is incorrect.")
