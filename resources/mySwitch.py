from PyQt5.QtCore import Qt, QRect
from PyQt5.QtGui import QPainter, QPixmap
from PyQt5.QtWidgets import QPushButton

class QSwitch(QPushButton):
    def __init__(self, parent=None):
        super(QSwitch, self).__init__(parent)
        self.checked = False
        self.setMinimumWidth(80)
        self.setMaximumWidth(80)
        self.setMinimumHeight(40)
        self.setMaximumHeight(40)

        # Textúrák betöltése
        self.day_pixmap = QPixmap("resources/images/day_icon.png")
        self.night_pixmap = QPixmap("resources/images/night_icon.png")

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)

        # Külső téglalap méretének és színének beállítása
        bgColor = Qt.black if self.checked else Qt.white
        penColor = Qt.white if self.checked else Qt.black
        painter.setBrush(bgColor)
        painter.setPen(penColor)
        painter.drawRoundedRect(QRect(1, 1, self.width() - 2, self.height() - 2), self.height() // 2,
                                self.height() // 2)

        # Kör méretének és pozíciójának dinamikus kiszámítása
        knobDiameter = self.height() - 8
        knobX = 4 if not self.checked else self.width() - knobDiameter - 4
        knobRect = QRect(knobX, 4, knobDiameter, knobDiameter)

        # Kör rajzolása (opcionális, ha átlátszó képet használsz)
        painter.setPen(Qt.NoPen)
        painter.drawEllipse(knobRect)

        # Kép skálázása és rajzolása a körön belül
        pixmap = self.night_pixmap if self.checked else self.day_pixmap
        painter.drawPixmap(knobRect, pixmap.scaled(knobRect.size(), Qt.KeepAspectRatio, Qt.SmoothTransformation))

    def mousePressEvent(self, event):
        self.checked = not self.checked
        self.update()  # Frissíti a widgetet, hogy tükrözze az állapotváltozást
        super(QSwitch, self).mousePressEvent(event)

    def isChecked(self):
        return self.checked

    def setChecked(self, checked):
        if self.checked != checked:
            self.checked = checked
            self.update()

