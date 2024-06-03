from PyQt5.QtWidgets import QTextEdit
from PyQt5.QtGui import QPainter, QColor
from PyQt5.QtCore import Qt

class PlaceholderTextEdit(QTextEdit):
    def __init__(self, placeholder_text, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.placeholder_text = placeholder_text
        self.show_placeholder = True
        self.textChanged.connect(self.check_placeholder_visibility)
        self.focused_in = False

    def check_placeholder_visibility(self):
        self.show_placeholder = not bool(self.toPlainText())
        self.viewport().update()

    def paintEvent(self, event):
        super().paintEvent(event)
        if self.show_placeholder and not self.focused_in:
            painter = QPainter(self.viewport())
            painter.setPen(QColor('gray'))
            painter.drawText(self.rect().adjusted(2, 2, -2, -2), Qt.AlignTop | Qt.AlignLeft, self.placeholder_text)

    def focusInEvent(self, event):
        super().focusInEvent(event)
        self.focused_in = True
        self.viewport().update()

    def focusOutEvent(self, event):
        super().focusOutEvent(event)
        self.focused_in = False
        self.check_placeholder_visibility()
