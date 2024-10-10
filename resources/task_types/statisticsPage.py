from PyQt5.QtCore import QAbstractTableModel, Qt
from PyQt5.QtGui import QPalette, QColor
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QHBoxLayout, QSpacerItem, QSizePolicy, QPushButton, \
    QTableView, QHeaderView


class StatisticsPage(QWidget):
    def __init__(self, db_manager, user_id, parent=None):
        super().__init__(parent)
        self.db_manager = db_manager
        self.user_id = user_id
        self.parent_window = parent
        self.initUI()

    def initUI(self):
        layout = QHBoxLayout()

        # Bal oldali táblázat létrehozása
        self.tasks_table = QTableView(self)
        self.tasks_table.setMinimumWidth(500)

        # Kijelölés letiltása
        self.tasks_table.setSelectionMode(QTableView.NoSelection)
        self.tasks_table.setEditTriggers(QTableView.NoEditTriggers)

        # Sor szélesség nyújtás letiltása
        self.tasks_table.horizontalHeader().setSectionsMovable(False)
        self.tasks_table.horizontalHeader().setSectionResizeMode(QHeaderView.Fixed)

        # Táblázat fejlécek automatikus nyújtása
        self.tasks_table.horizontalHeader().setStretchLastSection(True)
        self.tasks_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)

        # Feladatok lekérdezése és frissítése
        self.update_task_table()

        # Jobb oldali statisztikák panel
        self.stats_layout = QVBoxLayout()

        # Statisztikák lekérdezése és frissítése
        self.update_statistics()

        # Spacer, hogy középre legyenek a statisztikák
        self.stats_layout.addStretch()

        # Bezárás gomb
        close_button = QPushButton("Close", self)
        close_button.clicked.connect(self.parent_window.on_close_statistics)
        self.stats_layout.addWidget(close_button)

        # Jobb oldali panel beállítása
        self.stats_panel = QWidget(self)
        self.stats_panel.setLayout(self.stats_layout)

        # Layout beállítása a főablakhoz
        layout.addWidget(self.tasks_table)  # Bal oldalon a feladatok táblázata
        layout.addWidget(self.stats_panel)  # Jobb oldalon a statisztikák és bezárás gomb

        self.setLayout(layout)

    def update_task_table(self):
        # Lekérdezzük a felhasználó feladatait az adatbázisból
        user_tasks = self.db_manager.get_user_tasks(self.user_id)

        # Feladatok megjelenítése a táblázat modelljében
        self.task_table_model = TaskTableModel(user_tasks)
        self.tasks_table.setModel(self.task_table_model)

    def update_statistics(self):
        # Statisztikai adatok lekérdezése az adatbázisból
        stats = self.db_manager.get_user_statistics(self.user_id)

        # Statisztikai elemek törlése a frissítés előtt (spacert és gombot nem töröljük)
        for i in reversed(range(self.stats_layout.count() - 1)):
            widget = self.stats_layout.itemAt(i).widget()
            if widget is not None:
                widget.deleteLater()

        # Új statisztikai elemek hozzáadása
        total_tasks_label = QLabel(f"Total tasks: {stats['total_tasks']}")
        completed_tasks_label = QLabel(f"Completed tasks: {stats['completed_tasks']}")
        failures_label = QLabel(f"Total failures: {stats['total_failures']}")
        completion_rate_label = QLabel(f"Completion rate: {stats['completion_rate']:.2f}%")
        accuracy_label = QLabel(f"Accuracy: {stats['accuracy']:.2f}%")

        # Statisztikai elemek hozzáadása a layout-hoz
        self.stats_layout.insertWidget(0, total_tasks_label)
        self.stats_layout.insertWidget(1, completed_tasks_label)
        self.stats_layout.insertWidget(2, failures_label)
        self.stats_layout.insertWidget(3, completion_rate_label)
        self.stats_layout.insertWidget(4, accuracy_label)

    def set_theme(self, isDarkTheme):
        palette = self.palette()

        if isDarkTheme:
            # Sötét téma színek
            palette.setColor(QPalette.Window, QColor(53, 53, 53))
            palette.setColor(QPalette.WindowText, Qt.white)
            palette.setColor(QPalette.Base, QColor(25, 25, 25))
            palette.setColor(QPalette.AlternateBase, QColor(53, 53, 53))
            palette.setColor(QPalette.ToolTipBase, Qt.white)
            palette.setColor(QPalette.ToolTipText, Qt.white)
            palette.setColor(QPalette.Text, Qt.white)
            palette.setColor(QPalette.Button, QColor(53, 53, 53))
            palette.setColor(QPalette.ButtonText, Qt.white)
            palette.setColor(QPalette.BrightText, Qt.red)

            # Fejléc szín beállítása sötét témához
            self.tasks_table.horizontalHeader().setStyleSheet(
                "QHeaderView::section { background-color: rgb(53, 53, 53); color: white; }")
        else:
            # Világos téma színek
            palette.setColor(QPalette.Window, Qt.white)
            palette.setColor(QPalette.WindowText, Qt.black)
            palette.setColor(QPalette.Base, Qt.white)
            palette.setColor(QPalette.AlternateBase, Qt.white)
            palette.setColor(QPalette.ToolTipBase, Qt.black)
            palette.setColor(QPalette.ToolTipText, Qt.black)
            palette.setColor(QPalette.Text, Qt.black)
            palette.setColor(QPalette.Button, Qt.lightGray)
            palette.setColor(QPalette.ButtonText, Qt.black)
            palette.setColor(QPalette.BrightText, Qt.red)

            # Fejléc szín beállítása világos témához
            self.tasks_table.horizontalHeader().setStyleSheet(
                "QHeaderView::section { background-color: white; color: black; }")

        self.setPalette(palette)

    # 2. Betűméret beállítása függvény
    def set_font_size(self, size):
        font = self.font()
        font.setPointSize(size)
        self.setFont(font)

        # A meglévő widgetek betűméretének frissítése
        self.tasks_table.setFont(font)
        for i in range(self.stats_layout.count()):
            widget = self.stats_layout.itemAt(i).widget()
            if widget:
                widget.setFont(font)

class TaskTableModel(QAbstractTableModel):
    def __init__(self, tasks, parent=None):
        super().__init__(parent)
        self.tasks = tasks

    def rowCount(self, parent=None):
        return len(self.tasks)

    def columnCount(self, parent=None):
        return 3  # Három oszlop: Feladat neve, Teljesítve-e, Hibák száma

    def data(self, index, role=Qt.DisplayRole):
        if not index.isValid() or role != Qt.DisplayRole:
            return None

        task = self.tasks[index.row()]

        if index.column() == 0:
            return task[1]  # Feladat neve
        elif index.column() == 1:
            return "Completed" if task[2] == 1 else "Incomplete"  # Feladat státusza
        elif index.column() == 2:
            return task[3]  # Hibák száma

        return None

    def headerData(self, section, orientation, role=Qt.DisplayRole):
        if role == Qt.DisplayRole and orientation == Qt.Horizontal:
            if section == 0:
                return "Task Title"
            elif section == 1:
                return "Completed"
            elif section == 2:
                return "Failures"
        return None
