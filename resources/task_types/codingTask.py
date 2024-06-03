import sys
from contextlib import redirect_stdout
from io import StringIO

from PyQt5.QtCore import QSize, Qt, QRect
from PyQt5.QtGui import QIcon, QPainter, QTextFormat, QColor
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QTextEdit, QPushButton, QPlainTextEdit, QMessageBox


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


class CodeRunner(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.initUI()

    def initUI(self):
        self.code_editor = CodeEditor()
        self.output_window = QPlainTextEdit()
        self.output_window.setReadOnly(True)
        self.output_window.setMaximumHeight(100)

        self.run_button = QPushButton(QIcon('resources/images/run_button.png'), "", self)
        self.run_button.setIconSize(QSize(50, 100))
        self.run_button.setFixedSize(55, 100)
        self.run_button.clicked.connect(self.run_code)

        code_layout = QHBoxLayout()
        code_layout.addWidget(self.code_editor, 2)

        output_layout = QHBoxLayout()
        output_layout.addWidget(self.run_button)
        output_layout.addWidget(self.output_window)

        layout = QVBoxLayout()
        layout.addLayout(code_layout)
        layout.addLayout(output_layout)

        self.setLayout(layout)

    def test_user_code(self, user_code, correct_function_calls):
        # Először bontsuk részekre a megoldás mezőjét
        sections = correct_function_calls.split('\n')

        function_test_lines = []
        other_test_lines = []
        current_section = None

        for line in sections:
            if 'függvény teszt' in line:
                current_section = 'function_test'
            elif 'kiiratás' in line:
                current_section = 'print_check'
            else:
                if current_section == 'function_test':
                    function_test_lines.append(line.strip())
                elif current_section == 'print_check':
                    other_test_lines.append(line.strip())

        # A függvényhívások és az elvárt visszatérési értékek
        test_cases = []
        expected_outputs = []

        for call in function_test_lines:
            if call:
                function_call, expected_output = call.split('#')
                test_cases.append(function_call.strip())
                expected_outputs.append(expected_output.strip())

        # A kimenet ellenőrzése
        print_tests = []
        for check in other_test_lines:
            if 'print(' in check:
                print_tests.append(check.strip())

        # A felhasználó kódját futtatjuk
        try:
            user_namespace = {}
            exec(user_code, user_namespace)

            # Teszteljük a függvény visszatérési értékeit
            for i, test_case in enumerate(test_cases):
                result = eval(test_case, user_namespace)
                expected_result = eval(expected_outputs[i])
                if result != expected_result:
                    return False, f"Test failed: {test_case} expected {expected_result}, but got {result}"

            # Teszteljük a print outputokat
            output = StringIO()
            with redirect_stdout(output):
                for test in print_tests:
                    exec(test, user_namespace)
            printed_output = output.getvalue().strip().split('\n')

            for i, test in enumerate(print_tests):
                test_output = eval(test[test.find('(') + 1:test.find(')')], user_namespace)
                if str(test_output) != printed_output[i]:
                    return False, f"Print test failed: expected {test_output}, but got {printed_output[i]}"

        except Exception as e:
            return False, str(e)

        return True, "All tests passed."

    def run_code(self):
        user_code = self.code_editor.toPlainText()
        result, message = self.test_user_code(user_code, self.task_data['code_result'])
        self.output_window.setPlainText(message if result else f"Error: {message}")

    def clear(self):
        self.code_editor.clear()
        self.output_window.clear()

    def load_task(self, task_data):
        self.task_data = task_data
        self.code_editor.setPlainText(task_data['code_template'])
        self.output_window.clear()
