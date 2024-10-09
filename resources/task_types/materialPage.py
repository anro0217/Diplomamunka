from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton


class MaterialPage(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.initUI()
        self.start_task_callback = None

    def initUI(self):
        layout = QVBoxLayout()

        self.material_label = QLabel("")
        self.material_label.setAlignment(Qt.AlignTop)
        self.material_label.setWordWrap(True)
        layout.addWidget(self.material_label)

        self.start_task_button = QPushButton("Start Task", self)
        self.start_task_button.clicked.connect(self.start_task)
        layout.addWidget(self.start_task_button)

        self.setLayout(layout)

    def load_material(self, material):
        self.material_label.setText(material)

    def set_start_task_callback(self, callback):
        self.start_task_callback = callback

    def start_task(self):
        if self.start_task_callback:
            self.start_task_callback()
