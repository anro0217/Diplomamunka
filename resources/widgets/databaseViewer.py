from PyQt5.QtWidgets import QWidget, QVBoxLayout, QTableWidget, QTableWidgetItem, QHeaderView, QComboBox

class DatabaseViewer(QWidget):
    def __init__(self, db_manager):
        super().__init__()
        self.db_manager = db_manager
        self.initUI()

    def initUI(self):
        self.layout = QVBoxLayout(self)

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
        self.table_selector.model().removeRow(tables.index('sqlite_sequence'))

    def load_table_data(self, index):
        table_name = self.table_selector.itemText(index)
        data, columns = self.db_manager.get_table_data(table_name)
        if 'password' in columns:
            pwd_index = columns.index('password')
            columns.pop(pwd_index)
            data = [row[:pwd_index] + row[pwd_index+1:] for row in data]
        self.populate_table(data, columns)

    def populate_table(self, data, columns):
        self.data_table.clear()
        self.data_table.setRowCount(len(data))
        self.data_table.setColumnCount(len(columns))

        # Oszlopcímek beállítása
        self.data_table.setHorizontalHeaderLabels(columns)
        # Sorindexek elrejtése
        self.data_table.verticalHeader().setVisible(False)

        for row_index, row_data in enumerate(data):
            for column_index, cell_data in enumerate(row_data):
                self.data_table.setItem(row_index, column_index, QTableWidgetItem(str(cell_data)))

        # Oszlopok automatikus átméretezése
        self.data_table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeToContents)

    def get_selected_record_id(self):
        selected_indexes = self.data_table.selectionModel().selectedRows()
        if not selected_indexes:  # Ha nincs kiválasztott sor
            return None
        selected_row = selected_indexes[0].row()
        id_column_index = 0  # Feltételezzük, hogy az ID az első oszlopban van
        selected_record_id = self.data_table.item(selected_row, id_column_index).text()
        return int(selected_record_id)
