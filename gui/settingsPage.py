from PyQt5.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton
from PyQt5.QtCore import Qt

from database.database import DatabaseManager
from resources.widgets.mySlider import ClickableSlider
from resources.widgets.mySwitch import QSwitch
from resources.utils.globalSignals import globalSignals

global_theme_checked = False

class SettingsWindow(QWidget):

    def __init__(self, parent=None):
        super().__init__(parent, Qt.FramelessWindowHint | Qt.Tool | Qt.WindowStaysOnTopHint)
        self.db_manager = DatabaseManager('database/application.db')
        globalSignals.fontSizeChanged.connect(self.setFontSize)
        globalSignals.themeChanged.connect(self.setTheme)
        self.initUI()

    def initUI(self):
        mainLayout = QVBoxLayout(self)

        # Téma váltó kapcsoló elhelyezése a jobb felső sarokban
        topLayout = QHBoxLayout()
        self.theme_switch = QSwitch(self)

        self.theme_switch.setChecked(global_theme_checked)

        topLayout.addWidget(self.theme_switch, 0, Qt.AlignRight)
        mainLayout.addLayout(topLayout)

        # Adding the font size label and slider closely
        fontSizeLayout = QVBoxLayout()  # Creating a new vertical layout for tight spacing
        self.fontSizeLabel = QLabel("Font size", self)
        self.fontSizeLabel.setAlignment(Qt.AlignCenter | Qt.AlignBottom)
        fontSizeLayout.addWidget(self.fontSizeLabel)

        self.fontSizeSlider = ClickableSlider(Qt.Horizontal, self)
        self.fontSizeSlider.setMinimum(10)
        self.fontSizeSlider.setMaximum(21)
        self.fontSizeSlider.setValue(10)

        fontSizeLayout.addWidget(self.fontSizeSlider)

        mainLayout.addLayout(fontSizeLayout)

        self.fontSizeSlider.valueChanged.connect(lambda _:
                                                 globalSignals.fontSizeChanged.emit(self.fontSizeSlider.getValue()))
        #self.theme_switch.clicked.connect(lambda _: globalSignals.themeChanged.emit(self.theme_switch.isChecked()))

        self.theme_switch.clicked.connect(self.handleThemeSwitch)

        self.updateSliderValue()

        self.hide()

    def handleThemeSwitch(self):
        global global_theme_checked
        global_theme_checked = self.theme_switch.isChecked()

        # Kibocsátjuk a jelzést, hogy a téma megváltozott
        globalSignals.themeChanged.emit(global_theme_checked)

    def toggleVisibility(self, mainWindowGeometry):
        if self.isVisible():
            self.hide()
        else:
            self.panelWidth = 300
            self.panelHeight = mainWindowGeometry.height()
            self.panelX = mainWindowGeometry.x() + mainWindowGeometry.width()
            self.panelY = mainWindowGeometry.y()

            self.setGeometry(self.panelX, self.panelY, self.panelWidth, self.panelHeight)
            self.updateSliderValue()
            global global_theme_checked
            self.theme_switch.setChecked(global_theme_checked)
            self.show()
            self.raise_()

    def updateSliderValue(self):
        current_font_size = self.font().pointSize()
        self.fontSizeSlider.setValue(current_font_size)

    def updateLayout(self, size, theme):
        self.theme_switch.setChecked(theme)
        self.fontSizeSlider.setValue(size)

    def setTheme(self):
        if global_theme_checked:
            self.setStyleSheet("background-color: #333333; color: #ffffff;")
        else:
            self.setStyleSheet("background-color: #ffffff; color: #000000;")

    def setFontSize(self, size):
        font = self.font()
        font.setPointSize(size)
        self.setFont(font)
        self.fontSizeLabel.setFont(font)
        self.updateSliderValue()
