from PyQt5.QtWidgets import QApplication
from gui.loginPage import LoginPage
from gui.registrationPage import RegistrationWindow
import sys


def main():
    app = QApplication(sys.argv)

    # Létrehozzuk a két ablak példányát
    login_window = LoginPage()
    registration_window = RegistrationWindow(login_window=login_window)

    # Átadjuk a regisztrációs ablak referenciáját a bejelentkezési ablaknak
    login_window.registration_window = registration_window

    login_window.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
