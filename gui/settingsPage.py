from PyQt5.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout
from PyQt5.QtCore import Qt
from resources.widgets.mySwitch import QSwitch
from resources.utils.globalSignals import globalSignals


class SettingsWindow(QWidget):

    def __init__(self, parent=None):
        super().__init__(parent, Qt.FramelessWindowHint | Qt.Tool | Qt.WindowStaysOnTopHint)
        globalSignals.fontSizeChanged.connect(self.setFontSize)
        globalSignals.themeChanged.connect(self.setTheme)
        self.initUI()
        self.setFontSize(20)

    def initUI(self):
        mainLayout = QVBoxLayout(self)

        # Téma váltó kapcsoló elhelyezése a jobb felső sarokban
        topLayout = QHBoxLayout()
        self.theme_switch = QSwitch(self)
        topLayout.addWidget(self.theme_switch, 0, Qt.AlignRight)
        mainLayout.addLayout(topLayout)

        # Adding the font size label and slider closely
        # fontSizeLayout = QVBoxLayout()  # Creating a new vertical layout for tight spacing
        # self.fontSizeLabel = QLabel("Font size", self)
        # fontSizeLayout.addWidget(self.fontSizeLabel)

        # self.fontSizeSlider = ClickableSlider(Qt.Horizontal, self)
        # self.fontSizeSlider.setMinimum(10)
        # self.fontSizeSlider.setMaximum(30)
        # fontSizeLayout.addWidget(self.fontSizeSlider)

        # mainLayout.addLayout(fontSizeLayout)

        # self.fontSizeSlider.valueChanged.connect(lambda _:
        #                                          globalSignals.fontSizeChanged.emit(self.fontSizeSlider.getValue()))
        self.theme_switch.clicked.connect(lambda _: globalSignals.themeChanged.emit(self.theme_switch.isChecked()))

        self.hide()

    def toggleVisibility(self, mainWindowGeometry):
        if self.isVisible():
            self.hide()
        else:
            self.panelWidth = 300
            self.panelHeight = mainWindowGeometry.height()
            self.panelX = mainWindowGeometry.x() + mainWindowGeometry.width()
            self.panelY = mainWindowGeometry.y()

            self.setGeometry(self.panelX, self.panelY, self.panelWidth, self.panelHeight)
            self.show()
            self.raise_()

    def setTheme(self):
        if self.theme_switch.isChecked():
            self.setStyleSheet("background-color: #333333; color: #ffffff;")
        else:
            self.setStyleSheet("background-color: #ffffff; color: #000000;")

    def setFontSize(self, size):
        font = self.font()
        font.setPointSize(size)
        # self.fontSizeLabel.setFont(font)









