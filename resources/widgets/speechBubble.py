from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPainter, QPainterPath, QColor
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QTextEdit, QApplication


class SpeechBubble(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.Tool | Qt.WA_TranslucentBackground)  # Frissített ablakflag
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.setFixedSize(600, 300)

        layout = QVBoxLayout()
        self.text_edit = QTextEdit()
        self.text_edit.setReadOnly(True)
        self.text_edit.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.text_edit.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        layout.addWidget(self.text_edit)
        self.setLayout(layout)

        # Alapértelmezett világos téma
        self.isDarkTheme = False
        self.hide()

    def setText(self, text):
        self.text_edit.setPlainText(text)

    def getText(self):
        return self.text_edit.toPlainText()

    def paintEvent(self, event):
        super().paintEvent(event)
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)

        # Átlátszó háttér
        painter.fillRect(self.rect(), QColor(0, 0, 0, 0))

        # Kör alakú keret rajzolása a téma alapján
        path = QPainterPath()
        path.addRoundedRect(10, 10, self.width() - 20, self.height() - 20, 20, 20)

        if self.isDarkTheme:
            painter.setBrush(Qt.darkGray)
            painter.setPen(Qt.white)
        else:
            painter.setBrush(Qt.white)
            painter.setPen(Qt.black)

        painter.drawPath(path)

    def updateTheme(self, isDarkTheme):
        """Frissíti a megjelenést a kiválasztott téma alapján."""
        self.isDarkTheme = isDarkTheme

        if isDarkTheme:
            self.text_edit.setStyleSheet("""
                QTextEdit {
                    color: white;
                    background: transparent;
                    border: none;
                    padding: 10px;
                    border-radius: 10px;
                }
            """)
        else:
            self.text_edit.setStyleSheet("""
                QTextEdit {
                    color: black;
                    background: transparent;
                    border: none;
                    padding: 10px;
                    border-radius: 10px;
                }
            """)
        self.update()
