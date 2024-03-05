from PyQt5.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QTableWidget, QTableWidgetItem, QHeaderView, QComboBox


class DatabaseViewer(QWidget):
    def __init__(self, db_manager):
        super().__init__()
        self.db_manager = db_manager
        self.initUI()

    def initUI(self):
        self.layout = QVBoxLayout(self)

        # Táblák lenyíló menüje
        self.table_selector = QComboBox()
        self.layout.addWidget(self.table_selector)
        self.table_selector.currentIndexChanged.connect(self.load_table_data)

        # Adatok megjelenítésére szolgáló táblázat
        self.data_table = QTableWidget()
        self.data_table.setSelectionBehavior(QTableWidget.SelectRows)
        self.data_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.layout.addWidget(self.data_table)

        # Adatbázis táblák betöltése
        self.load_table_names()

    def load_table_names(self):
        tables = self.db_manager.get_table_names()
        self.table_selector.addItems(tables)

    def load_table_data(self, index):
        table_name = self.table_selector.itemText(index)
        data = self.db_manager.get_table_data(table_name)
        self.populate_table(data)

    def populate_table(self, data):
        self.data_table.clear()
        if data:
            self.data_table.setRowCount(len(data))
            self.data_table.setColumnCount(len(data[0]))
            for row_index, row_data in enumerate(data):
                for column_index, cell_data in enumerate(row_data):
                    self.data_table.setItem(row_index, column_index, QTableWidgetItem(str(cell_data)))
