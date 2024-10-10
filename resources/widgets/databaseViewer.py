from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QTableWidget, QTableWidgetItem, QHeaderView, QComboBox, QMenu, QAction

from resources.utils.globalSignals import globalSignals


class DatabaseViewer(QWidget):
    def __init__(self, db_manager, user_id, parent=None):
        super().__init__()
        self.db_manager = db_manager
        self.user_id = user_id
        self.parent_window = parent
        self.initUI()
        globalSignals.themeChanged.connect(self.toggle_theme)
        globalSignals.fontSizeChanged.connect(self.setFontSize)

    def initUI(self):
        self.layout = QVBoxLayout(self)

        self.table_selector = QComboBox()
        self.layout.addWidget(self.table_selector)
        self.table_selector.currentIndexChanged.connect(self.on_table_selector_changed)

        # Adatok megjelenítésére szolgáló táblázat
        self.data_table = QTableWidget()
        self.data_table.setSelectionBehavior(QTableWidget.SelectRows)
        self.data_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.layout.addWidget(self.data_table)

        # Adatbázis táblák betöltése
        self.load_table_names()

        user_settings = self.db_manager.load_user_settings(self.user_id)
        if user_settings:
            theme = user_settings.get('theme', 'light')  # Alapértelmezett téma világos
            if theme == 'dark':
                self.set_dark_mode()
            else:
                self.set_light_mode()

    def on_table_selector_changed(self, index):
        self.load_table_data(index)
        self.parent_window.set_button_states(index)

    def load_table_names(self):
        tables = self.db_manager.get_table_names()

        # Az 'sqlite_sequence' eltávolítása, ha létezik
        if 'sqlite_sequence' in tables:
            tables.remove('sqlite_sequence')

        # Sorrend beállítása
        ordered_tables = ['tasks', 'user_tasks', 'users', 'user_settings']
        other_tables = [table for table in tables if table not in ordered_tables]
        self.table_selector.addItems(ordered_tables + other_tables)

    def load_table_data(self, index):
        table_name = self.table_selector.itemText(index)
        data, columns = self.db_manager.get_table_data(table_name)
        if 'password' in columns:
            pwd_index = columns.index('password')
            columns.pop(pwd_index)
            data = [row[:pwd_index] + row[pwd_index + 1:] for row in data]

        self.populate_table(data, columns)

    def populate_table(self, data, columns):
        self.data_table.clear()
        self.data_table.setRowCount(len(data))
        self.data_table.setColumnCount(len(columns))

        # Oszlopcímek beállítása
        self.data_table.setHorizontalHeaderLabels(columns)
        # Sorindexek elrejtése
        self.data_table.verticalHeader().setVisible(False)

        # Ellenőrizzük, hogy a "tasks" tábla van-e kiválasztva
        is_tasks_table = self.table_selector.currentText() == "tasks"

        for row_index, row_data in enumerate(data):
            for column_index, cell_data in enumerate(row_data):
                item = QTableWidgetItem(str(cell_data))
                if is_tasks_table:
                    # Engedélyezett a szerkesztés csak a "tasks" táblában
                    item.setFlags(item.flags() | Qt.ItemIsEditable)
                else:
                    # Más táblák esetén a mezők nem szerkeszthetők
                    item.setFlags(item.flags() & ~Qt.ItemIsEditable)
                self.data_table.setItem(row_index, column_index, item)

        # Események kezelése
        try:
            self.data_table.itemChanged.disconnect(self.handle_item_changed)
        except TypeError:
            # Ha nincs csatlakoztatva, nem kell semmit tenni
            pass

        if is_tasks_table:
            self.data_table.itemChanged.connect(self.handle_item_changed)

        # Oszlopok automatikus átméretezése
        self.data_table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeToContents)

    def handle_item_changed(self, item):
        # Ha a felhasználó lenyomta az Enter-t, a rekordot frissítjük az adatbázisban
        row = item.row()
        column = item.column()
        new_value = item.text()
        table_name = self.table_selector.currentText()

        # Azonosító (feltételezzük, hogy az első oszlop az ID)
        record_id = self.data_table.item(row, 0).text()

        # Az oszlop neve, ahol módosítás történt
        column_name = self.data_table.horizontalHeaderItem(column).text()

        # Frissítjük az adatbázisban
        if table_name == "tasks":
            task_data = self.db_manager.get_task_by_id(int(record_id))
            task_data[column_name] = new_value  # Frissítjük a módosított oszlopot
            self.db_manager.update_task(
                task_id=int(record_id),
                title=task_data['title'],
                description=task_data['description'],
                task_type=task_data['type'],
                code_template=task_data['code_template'],
                code_result=task_data['code_result'],
                drag_drop_items=task_data['drag_drop_items'],
                matching_pairs=task_data['matching_pairs'],
                quiz_question=task_data['quiz_question'],
                quiz_options=task_data['quiz_options'],
                quiz_answer=task_data['quiz_answer'],
                debugging_code=task_data['debugging_code'],
                correct_code=task_data['correct_code'],
                material=task_data['material']
            )

    def get_selected_record_id(self):
        selected_indexes = self.data_table.selectionModel().selectedRows()
        if not selected_indexes:  # Ha nincs kiválasztott sor
            return None
        selected_row = selected_indexes[0].row()
        id_column_index = 0  # Feltételezzük, hogy az ID az első oszlopban van
        selected_record_id = self.data_table.item(selected_row, id_column_index).text()
        return int(selected_record_id)

    def get_selected_record_ids(self):
        selected_indexes = self.data_table.selectionModel().selectedRows()
        if not selected_indexes:  # Ha nincs kiválasztott sor
            return []

        selected_record_ids = []
        id_column_index = 0  # Feltételezzük, hogy az ID az első oszlopban van

        for index in selected_indexes:
            selected_row = index.row()
            selected_record_id = self.data_table.item(selected_row, id_column_index).text()
            selected_record_ids.append(int(selected_record_id))

        return selected_record_ids

    def setFontSize(self, size):
        font = QFont()
        font.setPointSize(size)

        self.data_table.setFont(font)

        header_font = self.data_table.horizontalHeader().font()
        header_font.setPointSize(size)
        self.data_table.horizontalHeader().setFont(header_font)

        self.table_selector.setFont(font)

    def toggle_theme(self, is_dark_mode):
        if is_dark_mode:
            self.set_dark_mode()
        else:
            self.set_light_mode()

    def set_dark_mode(self):
        # Sötét téma stílus beállítása
        dark_style = """
        QHeaderView::section {
            background-color: #2b2b2b;
            color: white;
            padding: 4px;
            border: 1px solid #444444;
        }
        """
        self.data_table.setStyleSheet(dark_style)
        self.setStyleSheet("background-color: #333333; color: #ffffff;")

    def set_light_mode(self):
        # Világos téma stílus beállítása
        light_style = """
        QHeaderView::section {
            background-color: #f0f0f0;
            color: black;
            padding: 4px;
            border: 1px solid #dcdcdc;
        }
        """
        self.data_table.setStyleSheet(light_style)
        self.setStyleSheet("background-color: #ffffff; color: #000000;")


