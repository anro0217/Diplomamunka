from PyQt5.QtCore import QStringListModel
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QListView, QHBoxLayout, QSpacerItem, QSizePolicy, QPushButton

class StatisticsPage(QWidget):
    def __init__(self, db_manager, user_id, parent=None):
        super().__init__(parent)
        self.db_manager = db_manager
        self.user_id = user_id
        self.parent_window = parent
        self.initUI()

    def initUI(self):
        self.stats_spacer = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)
        # Layout beállítása
        layout = QHBoxLayout()

        # Bal oldali görgethető lista létrehozása
        self.tasks_list = QListView()
        self.tasks_list.setMinimumWidth(300)  # Minimális szélesség beállítása

        # Feladatok lekérdezése a db_managerből
        self.update_task_list()  # Feladatok frissítése

        # Jobb oldali statisztikák panel
        self.stats_layout = QVBoxLayout()

        # Statisztikák lekérdezése
        self.update_statistics()  # Statisztikák frissítése

        # Jobb oldali panel középre igazítása
        self.stats_layout.addItem(self.stats_spacer)

        # Gomb létrehozása a bezáráshoz
        close_button = QPushButton("Close")
        close_button.clicked.connect(self.parent_window.on_close_statistics)
        self.stats_layout.addWidget(close_button)  # Gomb hozzáadása a statisztikák panelhez

        # A statisztikák panel beállítása
        self.stats_panel = QWidget()
        self.stats_panel.setLayout(self.stats_layout)

        layout.addWidget(self.tasks_list)
        layout.addWidget(self.stats_panel)

        # Layout beállítása
        self.setLayout(layout)

    def update_task_list(self):
        tasks = self.db_manager.get_tasks()  # Feladatok lekérdezése
        task_titles = [task['title'] for task in tasks]  # Feladatok neveinek listája

        # Model létrehozása a feladatok neveivel
        model = QStringListModel(task_titles)  # task_titles a feladatok neveivel
        self.tasks_list.setModel(model)

    def update_statistics(self):
        stats = self.db_manager.get_user_statistics(self.user_id)

        # Statisztikai elemek törlése a frissítés előtt, kivéve a spacer-t és a gombot
        for i in reversed(range(self.stats_layout.count())):
            widget = self.stats_layout.itemAt(i).widget()
            if widget is not None and not isinstance(widget, QPushButton):
                widget.deleteLater()

        # Statisztikai elemek létrehozása
        total_tasks_label = QLabel(f"Total tasks: {stats['total_tasks']}")
        completed_tasks_label = QLabel(f"Completed tasks: {stats['completed_tasks']}")
        failures_label = QLabel(f"Total failures: {stats['total_failures']}")
        completion_rate_label = QLabel(f"Completion rate: {stats['completion_rate']:.2f}%")
        accuracy_label = QLabel(f"Accuracy: {stats['accuracy']:.2f}%")

        # Statisztikai elemek hozzáadása a spacer és a gomb fölé
        self.stats_layout.insertWidget(self.stats_layout.count() - 2, total_tasks_label)
        self.stats_layout.insertWidget(self.stats_layout.count() - 2, completed_tasks_label)
        self.stats_layout.insertWidget(self.stats_layout.count() - 2, failures_label)
        self.stats_layout.insertWidget(self.stats_layout.count() - 2, completion_rate_label)
        self.stats_layout.insertWidget(self.stats_layout.count() - 2, accuracy_label)
