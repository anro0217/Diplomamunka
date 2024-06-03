from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QGridLayout, QPushButton, QMessageBox, QSpacerItem, QSizePolicy
from PyQt5.QtCore import Qt, QPoint
from PyQt5.QtGui import QPainter, QPen, QCursor
import random

class ConnectionPoint(QPushButton):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setFixedSize(20, 20)
        self.setStyleSheet("background-color: black; border-radius: 10px;")
        self.connected_line = None  # Tárolja a csatlakoztatott vonalat

    def enterEvent(self, event):
        self.setStyleSheet("background-color: red; border-radius: 10px;")

    def leaveEvent(self, event):
        self.setStyleSheet("background-color: black; border-radius: 10px;")

class Line:
    def __init__(self, start, end):
        self.start = start
        self.end = end

class MatchingTask(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.initUI()

    def initUI(self):
        self.layout = QVBoxLayout()

        self.grid_layout = QGridLayout()
        self.layout.addLayout(self.grid_layout)

        self.left_points = []
        self.right_points = []
        self.lines = []
        self.current_line = None
        self.drawing = False
        self.fixed_point = None

        spacer = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)
        self.layout.addItem(spacer)

        self.check_button = QPushButton("Check Pairs", self)
        self.check_button.setFixedSize(100, 30)
        self.check_button.clicked.connect(self.check_pairs)
        self.layout.addWidget(self.check_button, alignment=Qt.AlignBottom)

        self.setLayout(self.layout)

    def load_task(self, task_data):
        self.task_data = task_data
        self.clear_layout()
        pairs = task_data['matching_pairs'].split('\n')
        left_items = [pair.split(':')[0] for pair in pairs]
        right_items = [pair.split(':')[1] for pair in pairs]

        random.shuffle(left_items)
        random.shuffle(right_items)

        for i, item in enumerate(left_items):
            label = QLabel(item)
            self.grid_layout.addWidget(label, i, 0, alignment=Qt.AlignRight)
            point = ConnectionPoint()
            point.mousePressEvent = self.create_mouse_press_event_handler(point)
            self.left_points.append((point, item))
            self.grid_layout.addWidget(point, i, 1, alignment=Qt.AlignLeft)

        for i, item in enumerate(right_items):
            point = ConnectionPoint()
            point.mousePressEvent = self.create_mouse_press_event_handler(point)
            self.right_points.append((point, item))
            self.grid_layout.addWidget(point, i, 2, alignment=Qt.AlignRight)
            label = QLabel(item)
            self.grid_layout.addWidget(label, i, 3, alignment=Qt.AlignLeft)

        for i in range(len(left_items)):
            self.grid_layout.setRowMinimumHeight(i, 50)

        self.grid_layout.setColumnStretch(1, 1)
        self.grid_layout.setColumnStretch(2, 1)

    def clear_layout(self):
        for i in reversed(range(self.grid_layout.count())):
            widget = self.grid_layout.itemAt(i).widget()
            if widget is not None:
                widget.setParent(None)
        self.left_points = []
        self.right_points = []
        self.lines = []
        self.current_line = None
        self.drawing = False
        self.fixed_point = None
        self.update()

    def create_mouse_press_event_handler(self, point):
        def handler(event):
            if self.drawing:
                self.end_drawing(point)
            else:
                self.start_drawing(point)
        return handler

    def start_drawing(self, point):
        if point.connected_line is not None:
            # Vonatkoztatási pont áthelyezése
            self.current_line = point.connected_line
            if self.current_line.start == point:
                self.fixed_point = self.current_line.end
                self.current_line.start = None
            else:
                self.fixed_point = self.current_line.start
                self.current_line.end = None
            point.connected_line = None
            self.drawing = True
        else:
            # Új vonal rajzolásának kezdete
            self.current_line = Line(point, None)
            self.fixed_point = point
            self.drawing = True
            self.update()

    def end_drawing(self, point):
        if self.current_line and self.fixed_point:
            # Azonos oszlopban lévő pontok esetén nem csatlakoztathatunk
            if point == self.fixed_point or (point in [p for p, _ in self.left_points] and self.fixed_point in [p for p, _ in self.left_points]) or (point in [p for p, _ in self.right_points] and self.fixed_point in [p for p, _ in self.right_points]):
                self.remove_line(self.current_line)
                self.current_line = None
                self.drawing = False
                self.fixed_point = None
                self.update()
                return
            # Már csatlakoztatott pontok esetén nem csatlakoztathatunk mégegyszer
            if point.connected_line is not None:
                return
            # Vonal végpontjainak beállítása
            if self.current_line.start is None:
                self.current_line.start = point
            else:
                self.current_line.end = point
            self.lines.append(self.current_line)
            self.current_line.start.connected_line = self.current_line
            self.current_line.end.connected_line = self.current_line
            self.current_line = None
            self.drawing = False
            self.fixed_point = None
            self.update()

    def remove_line(self, line):
        if line.start:
            line.start.connected_line = None
        if line.end:
            line.end.connected_line = None
        if line in self.lines:
            self.lines.remove(line)
        self.update()

    def mouseMoveEvent(self, event):
        if self.drawing and self.current_line and self.fixed_point:
            self.update()

    def paintEvent(self, event):
        super().paintEvent(event)
        painter = QPainter(self)
        pen = QPen(Qt.black, 2)
        painter.setPen(pen)
        for line in self.lines:
            if line.start and line.end:
                start_pos = line.start.mapTo(self, QPoint(line.start.width() // 2, line.start.height() // 2))
                end_pos = line.end.mapTo(self, QPoint(line.end.width() // 2, line.end.height() // 2))
                painter.drawLine(start_pos, end_pos)
        if self.drawing and self.current_line and self.fixed_point:
            start_pos = self.fixed_point.mapTo(self, QPoint(self.fixed_point.width() // 2, self.fixed_point.height() // 2))
            end_pos = self.mapFromGlobal(QCursor.pos())
            painter.drawLine(start_pos, end_pos)
        self.setMouseTracking(True)

    def check_pairs(self):
        correct_pairs = self.task_data['matching_pairs'].strip().split('\n')
        user_pairs = []

        for line in self.lines:
            start_item = next((item for point, item in self.left_points if point == line.start), None)
            end_item = next((item for point, item in self.right_points if point == line.end), None)
            if start_item and end_item:
                user_pairs.append(f"{start_item}:{end_item}")
            else:
                start_item = next((item for point, item in self.right_points if point == line.start), None)
                end_item = next((item for point, item in self.left_points if point == line.end), None)
                if start_item and end_item:
                    user_pairs.append(f"{end_item}:{start_item}")

        if set(user_pairs) == set(correct_pairs):
            QMessageBox.information(self, "Correct", "Your solution is correct!")
        else:
            QMessageBox.warning(self, "Incorrect", "Your solution is incorrect.")
