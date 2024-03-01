from PyQt5.QtWidgets import QApplication
from gui.loginPage import LoginWindow
from gui.mainPage import MainWindow
from gui.registrationPage import RegistrationWindow
import sys


def main():
    app = QApplication(sys.argv)

    # Csak a fő ablak példányosítása
    main_window = MainWindow()

    # Az ablakok közötti referencia már nem szükséges itt
    main_window.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
