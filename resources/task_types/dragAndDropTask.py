import random
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QListWidget, QListWidgetItem, QMessageBox, QPushButton


class DragAndDropTask(QWidget):
    def __init__(self, db_manager, parent=None):
        super().__init__(parent)
        self.db_manager = db_manager
        self.parent_window = parent
        self.initUI()

    def initUI(self):
        layout = QVBoxLayout()

        self.list_widget = QListWidget()
        layout.addWidget(self.list_widget)
        self.list_widget.setDragDropMode(QListWidget.InternalMove)

        self.check_button = QPushButton("Check Order", self)
        #self.check_button.setFixedSize(100, 30)
        self.check_button.clicked.connect(self.check_order)
        layout.addWidget(self.check_button)

        self.setLayout(layout)

    def load_task(self, task_data, user_id):
        self.task_data = task_data
        self.user_id = user_id
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
            if self.parent_window and not self.parent_window.is_admin:
                self.db_manager.mark_task_as_completed(self.user_id, self.task_data['id'])
                self.parent_window.update_lessons_list()
                self.parent_window.get_next_task(self.task_data['id'])
        else:
            QMessageBox.warning(self, "Incorrect", "Your solution is incorrect.")
            if self.parent_window and not self.parent_window.is_admin:
                self.db_manager.increment_failure_count(self.user_id, self.task_data['id'])
