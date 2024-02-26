from PyQt5.QtWidgets import QApplication
from gui.loginPage import LoginPage
import sys

def main():
    app = QApplication(sys.argv)
    window = LoginPage()
    window.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
