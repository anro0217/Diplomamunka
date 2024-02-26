from PyQt5.QtCore import pyqtSignal, QObject


class GlobalSignals(QObject):
    # Definiálj egy jelzést, ami egy egész számot (a kívánt betűméretet) továbbít
    fontSizeChanged = pyqtSignal(int)

    # Definiálj egy jelzést a téma változtatására
    themeChanged = pyqtSignal(bool)  # True a sötét módhoz, False a világos módhoz


# Példányosítsd a jelzéseket
globalSignals = GlobalSignals()
