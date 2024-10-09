from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication
from gui.loginPage import LoginWindow
import sys


def main():
    app = QApplication(sys.argv)
    login_window = LoginWindow()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
