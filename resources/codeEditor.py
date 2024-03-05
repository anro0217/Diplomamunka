import sys
from contextlib import redirect_stdout
from io import StringIO

from PyQt5.QtCore import Qt, QRect, QSize
from PyQt5.QtGui import QPainter, QTextFormat, QColor
from PyQt5.QtWidgets import QTextEdit, QPlainTextEdit, QWidget


class LineNumberArea(QWidget):
    def __init__(self, editor):
        super().__init__(editor)
        self.code_editor = editor

    def sizeHint(self):
        return QSize(self.code_editor.line_number_area_width(), 0)

    def paintEvent(self, event):
        self.code_editor.line_number_area_paint_event(event)

class CodeEditor(QPlainTextEdit):
    def __init__(self):
        super().__init__()
        self.line_number_area = LineNumberArea(self)

        self.blockCountChanged.connect(self.update_line_number_area_width)
        self.updateRequest.connect(self.update_line_number_area)
        self.cursorPositionChanged.connect(self.highlight_current_line)

        self.update_line_number_area_width(0)
        self.highlight_current_line()

    def line_number_area_width(self):
        digits = 1
        max_num = max(1, self.blockCount())
        while max_num >= 10:
            max_num /= 10
            digits += 1
        space = 3 + self.fontMetrics().width('9') * digits
        return space

    def update_line_number_area_width(self, _):
        self.setViewportMargins(self.line_number_area_width(), 0, 0, 0)

    def update_line_number_area(self, rect, dy):
        if dy:
            self.line_number_area.scroll(0, dy)
        else:
            self.line_number_area.update(0, rect.y(), self.line_number_area.width(), rect.height())

        if rect.contains(self.viewport().rect()):
            self.update_line_number_area_width(0)

    def resizeEvent(self, event):
        super().resizeEvent(event)
        cr = self.contentsRect()
        self.line_number_area.setGeometry(QRect(cr.left(), cr.top(), self.line_number_area_width(), cr.height()))

    def highlight_current_line(self):
        extra_selections = []
        if not self.isReadOnly():
            selection = QTextEdit.ExtraSelection()
            line_color = QColor(Qt.yellow).lighter(160)
            selection.format.setBackground(line_color)
            selection.format.setProperty(QTextFormat.FullWidthSelection, True)
            selection.cursor = self.textCursor()
            selection.cursor.clearSelection()
            extra_selections.append(selection)
        self.setExtraSelections(extra_selections)

    def line_number_area_paint_event(self, event):
        painter = QPainter(self.line_number_area)
        painter.fillRect(event.rect(), Qt.lightGray)

        block = self.firstVisibleBlock()
        block_number = block.blockNumber()
        top = self.blockBoundingGeometry(block).translated(self.contentOffset()).top()
        bottom = top + self.blockBoundingRect(block).height()

        # A LineNumberArea szélességének megszerzése
        line_number_area_width = self.line_number_area.sizeHint().width()

        # A font méretének beállítása
        font = painter.font()
        font.setPointSize(font.pointSize() + 2)  # Állítsd be a kívánt méretre
        painter.setFont(font)

        while block.isValid() and top <= event.rect().bottom():
            if block.isVisible() and bottom >= event.rect().top():
                number = str(block_number + 1)
                painter.setPen(Qt.black)

                # Y pozíció számításának módosítása a szám középre igazításához
                height = self.blockBoundingRect(block).height()
                y_position = top + (height - painter.fontMetrics().height()) / 2

                painter.drawText(0, int(y_position), line_number_area_width,
                                 painter.fontMetrics().height(), Qt.AlignCenter, number)

            block = block.next()
            top = bottom
            bottom = top + self.blockBoundingRect(block).height()
            block_number += 1

    def paintEvent(self, event):
        super().paintEvent(event)
        self.line_number_area_paint_event(event)

    def sizeHint(self):
        return QSize(self.line_number_area_width(), 0)

    def run_code_and_capture_output(self):
        code = self.toPlainText()
        output = StringIO()
        with redirect_stdout(output):
            try:
                exec(code, {})
            except Exception as e:
                print(str(e), file=sys.stderr)
        return output.getvalue()

    def keyPressEvent(self, e):
        if e.key() == Qt.Key_Tab:
            cursor = self.textCursor()
            cursor.insertText("    ")  # insert 4 spaces
        else:
            super().keyPressEvent(e)  # Ensure the base class event is called