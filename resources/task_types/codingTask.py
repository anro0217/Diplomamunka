import sys
from contextlib import redirect_stdout
from io import StringIO

from PyQt5.QtCore import QSize, Qt, QRect
from PyQt5.QtGui import QIcon, QPainter, QTextFormat, QColor
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QTextEdit, QPushButton, QPlainTextEdit, QMessageBox

from resources.utils.globalSignals import globalSignals


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
        self.is_dark_mode = False

        self.blockCountChanged.connect(self.update_line_number_area_width)
        self.updateRequest.connect(self.update_line_number_area)
        self.cursorPositionChanged.connect(self.on_cursor_position_changed)

        self.update_line_number_area_width(0)
        self.highlight_current_line()
        #globalSignals.themeChanged.connect(self.on_theme_changed)

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

    def highlight_current_line(self, is_dark_mode=False):
        extra_selections = []
        if not self.isReadOnly():
            selection = QTextEdit.ExtraSelection()
            line_color = self.get_highlight_color(is_dark_mode)
            selection.format.setBackground(line_color)
            selection.format.setProperty(QTextFormat.FullWidthSelection, True)
            selection.cursor = self.textCursor()
            selection.cursor.clearSelection()
            extra_selections.append(selection)
        self.setExtraSelections(extra_selections)

    def get_highlight_color(self, is_dark_mode=False):
        if is_dark_mode:
            return QColor(Qt.green).lighter(140)
        else:
            return QColor(Qt.yellow).lighter(160)

    def on_cursor_position_changed(self):
        self.highlight_current_line(self.is_dark_mode)

    def on_theme_changed(self, is_dark_mode):
        self.is_dark_mode = is_dark_mode
        self.highlight_current_line(is_dark_mode)

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

    def set_font_size(self, size):
        """Sets the font size for the code editor."""
        font = self.font()
        font.setPointSize(size)
        self.setFont(font)

        # Also update the font size in the line number area
        self.line_number_area.update()

    def set_theme(self, is_dark_mode):
        """Sets the theme of the editor to dark or light mode."""
        self.is_dark_mode = is_dark_mode
        if is_dark_mode:
            # Dark mode: Black background, light text
            self.setStyleSheet("""
                QPlainTextEdit {
                    background-color: #2b2b2b;
                    color: #dcdcdc;
                }
            """)
            self.line_number_area.setStyleSheet("background-color: #313335; color: #dcdcdc;")
        else:
            # Light mode: White background, dark text
            self.setStyleSheet("""
                QPlainTextEdit {
                    background-color: #ffffff;
                    color: #000000;
                }
            """)
            self.line_number_area.setStyleSheet("background-color: #f0f0f0; color: #000000;")

        self.highlight_current_line(is_dark_mode)


class CodeRunner(QWidget):
    def __init__(self, db_manager, parent=None):
        super().__init__(parent)
        self.db_manager = db_manager
        self.parent_window = parent
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

    def run_code(self):
        result, message = self.test_user_code(self.code_editor.toPlainText(), self.task_data['code_result'])
        if result:
            QMessageBox.information(self, "Correct", "Your solution is correct!")
            if self.parent_window and not self.parent_window.is_admin:
                self.db_manager.mark_task_as_completed(self.user_id, self.task_data['id'])
                self.parent_window.update_lessons_list()
                self.parent_window.get_next_task(self.task_data['id'])
        else:
            QMessageBox.warning(self, "Incorrect", message)
            if self.parent_window and not self.parent_window.is_admin:
                self.db_manager.increment_failure_count(self.user_id, self.task_data['id'])

    def test_user_code(self, code_editor_input, test_cases):
        # 1. Check if only the function body was modified
        template_lines = self.task_data['code_template'].splitlines()
        user_code_lines = code_editor_input.splitlines()

        # Check the function header and the print statement at the end
        if user_code_lines[0] != template_lines[0] or user_code_lines[-1] != template_lines[-1]:
            return False, "You cannot modify the function header or the print statement at the end!"

        # Ensure that the function body has been modified (after the comment)
        if user_code_lines[1] == template_lines[1]:
            return False, "You haven't modified the function body yet!"

        # 2. Run the user's code and capture output
        output = StringIO()
        user_globals = {}
        try:
            with redirect_stdout(output):
                exec(code_editor_input, user_globals)
            # Output the result to the output window
            self.output_window.setPlainText(output.getvalue())
        except Exception as e:
            return False, f"Error occurred while running the code: {str(e)}"

        # 3. Check the provided test cases and calculate the success rate
        total_tests = 0
        passed_tests = 0

        for test_case in test_cases.splitlines():
            if test_case.strip():  # Skip empty lines
                total_tests += 1

                # Split the test case into input and expected output
                test_input, expected_output = test_case.split('#')
                test_input = test_input.strip()
                expected_output = expected_output.strip()

                # Run the test case
                try:
                    actual_output = eval(test_input, user_globals)
                    if str(actual_output) == expected_output:
                        passed_tests += 1
                except Exception:
                    continue  # Test fails if any exception occurs

        # Calculate the percentage of passed tests
        success_rate = (passed_tests / total_tests) * 100 if total_tests > 0 else 0

        # Provide feedback based on success rate
        if success_rate == 100:
            return True, ""
        if success_rate > 66:
            return False, "Almost correct, but not perfect."
        elif success_rate > 33:
            return False, "Something is still wrong."
        else:
            return False, "Incorrect solution."

    def clear(self):
        self.code_editor.clear()
        self.output_window.clear()

    def load_task(self, task_data, user_id):
        self.task_data = task_data
        self.user_id = user_id
        self.code_editor.setPlainText(task_data['code_template'])
        self.output_window.clear()

    def set_theme(self, is_dark_mode):
        self.code_editor.set_theme(is_dark_mode)

    def set_font_size(self, size):
        self.code_editor.set_font_size(size)
