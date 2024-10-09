from PyQt5.QtWidgets import QApplication, QTextEdit, QVBoxLayout, QWidget
from PyQt5.QtGui import QFont

class TestWindow(QWidget):
    def __init__(self):
        super().__init__()

        self.text_edit1 = QTextEdit()
        self.text_edit1.setPlaceholderText("Enter the code template here")

        self.text_edit2 = QTextEdit()
        self.text_edit2.setPlaceholderText("Enter the code result here")

        layout = QVBoxLayout()
        layout.addWidget(self.text_edit1)
        layout.addWidget(self.text_edit2)
        self.setLayout(layout)

        self.setFontSize(20)  # Állítsuk be a betűméretet 20-ra tesztként

    def setFontSize(self, size):
        font = QFont()
        font.setPointSize(size)
        self.text_edit1.setFont(font)
        self.text_edit2.setFont(font)

if __name__ == "__main__":
    app = QApplication([])
    window = TestWindow()
    window.show()
    app.exec_()
