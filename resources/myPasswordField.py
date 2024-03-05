from PyQt5.QtWidgets import QLineEdit, QPushButton, QStyle
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import Qt, QSize


class PasswordLineEdit(QLineEdit):
    def __init__(self, parent=None):
        super().__init__(parent)

        # Az ikonok elérési útjainak beállítása
        self.show_icon_path = 'resources/images/to_hide.png'
        self.hide_icon_path = 'resources/images/to_show.png'

        self.setEchoMode(QLineEdit.Password)

        # Jelszó láthatóságát váltó gomb létrehozása
        self.toggle_password_button = QPushButton(self)
        self.toggle_password_button.setIcon(QIcon(self.show_icon_path))
        self.toggle_password_button.setIconSize(QSize(30, 30))  # Nagyobb ikon méret beállítása
        self.toggle_password_button.setFixedSize(30, 30)  # Nagyobb gomb méret
        self.toggle_password_button.setStyleSheet("background: transparent; border: none;")
        self.toggle_password_button.setCursor(Qt.PointingHandCursor)

        # Itt állítjuk be, hogy a gomb ne legyen fókuszálható a tabulátorral
        self.toggle_password_button.setFocusPolicy(Qt.NoFocus)

        self.toggle_password_button.pressed.connect(self.show_password)
        self.toggle_password_button.released.connect(self.hide_password)

        # A gomb elhelyezése a beviteli mezőben
        self.setButtonPosition()

    def setButtonPosition(self):
        frame_width = self.style().pixelMetric(QStyle.PM_DefaultFrameWidth)
        button_size = self.toggle_password_button.size()
        x_position = self.rect().right() - frame_width - button_size.width() - 10
        y_position = int((self.rect().height() - button_size.height()) / 2)  # Kerekítés int-re
        self.toggle_password_button.move(x_position, y_position)

    def resizeEvent(self, event):
        self.setButtonPosition()
        super().resizeEvent(event)

    def show_password(self):
        self.setEchoMode(QLineEdit.Normal)
        self.toggle_password_button.setIcon(QIcon(self.hide_icon_path))

    def hide_password(self):
        self.setEchoMode(QLineEdit.Password)
        self.toggle_password_button.setIcon(QIcon(self.show_icon_path))
