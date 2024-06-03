from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPainter, QPainterPath
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QTextEdit, QApplication

class SpeechBubble(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowFlags(Qt.Popup | Qt.FramelessWindowHint)
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.setFixedSize(600, 300)
        self.setStyleSheet("""
            QTextEdit {
                background: transparent;
                border: none;
                padding: 10px;
                border-radius: 10px;
            }
            QTextEdit QScrollBar:vertical {
                width: 0px;
            }
        """)
        layout = QVBoxLayout()
        self.text_edit = QTextEdit()
        self.text_edit.setReadOnly(True)
        self.text_edit.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.text_edit.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        layout.addWidget(self.text_edit)
        self.setLayout(layout)

    def setText(self, text):
        self.text_edit.setPlainText(text)

    def getText(self):
        return self.text_edit.toPlainText()

    def paintEvent(self, event):
        super().paintEvent(event)
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)

        # Kör alakú keret rajzolása
        path = QPainterPath()
        path.addRoundedRect(10, 10, self.width() - 20, self.height() - 20, 20, 20)

        painter.setBrush(Qt.white)
        painter.setPen(Qt.black)
        painter.drawPath(path)