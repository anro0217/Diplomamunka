from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QStyleOptionSlider, QSlider

class ClickableSlider(QSlider):
    def __init__(self, orientation, parent=None):
        super().__init__(orientation, parent)

    def mousePressEvent(self, event):
        # Eredeti kattintás alapú logika
        opt = self.style().subControlRect(self.style().CC_Slider, self.sliderOption(), self.style().SC_SliderGroove,
                                          self)
        if self.orientation() == Qt.Horizontal:
            val = self.minimum() + ((self.maximum() - self.minimum()) * (event.x() - opt.x())) / opt.width()
            self.setValue(int(round(val)))
        else:  # Függőleges csúszka esetén
            val = self.minimum() + ((self.maximum() - self.minimum()) * (event.y() - opt.y())) / opt.height()
            self.setValue(int(round(val)))

        event.accept()
        super().mousePressEvent(event)

    def sliderOption(self):
        # A csúszka aktuális állapotának létrehozása
        option = QStyleOptionSlider()
        self.initStyleOption(option)
        return option

    def getValue(self):
        return self.value()
