from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton, QApplication


class WelcomePage(QWidget):  # TODO: megcsinálni a kezdőoldalt (mondjuk nyíl, vagy ikon megjelölés jelölje hova kell kattintani)
    def __init__(self, parent=None):
        super().__init__(parent)

        # Layout beállítása
        layout = QVBoxLayout()

        # Üdvözlő üzenet
        self.welcome_label = QLabel("Welcome to the Programming Language Learning Assistant!")
        self.welcome_label.setStyleSheet("font-size: 24px; font-weight: bold;")

        # Leírás
        self.description_label = QLabel(
            "This application helps you learn programming languages.\n"
            "Explore different languages, complete practical tasks,\n"
            "and track your progress!"
        )
        self.description_label.setStyleSheet("font-size: 16px;")

        # Widget elemek hozzáadása a layouthoz
        layout.addWidget(self.welcome_label)
        layout.addWidget(self.description_label)

        self.setLayout(layout)
