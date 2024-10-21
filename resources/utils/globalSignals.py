from PyQt5.QtCore import pyqtSignal, QObject


class GlobalSignals(QObject):
    fontSizeChanged = pyqtSignal(int)
    themeChanged = pyqtSignal(bool)


globalSignals = GlobalSignals()
