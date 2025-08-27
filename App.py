import sys
import json
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QPushButton,
    QLineEdit, QSpinBox, QTableWidget, QTableWidgetItem,
    QMessageBox, QFormLayout, QDialog, QInputDialog
)
import Write
import practice  # Your CLI-based backend logic (we’ll reuse createDatabase if needed)


class DatabaseManager(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Loadable")
        self.setGeometry(200, 200, 600, 400)

        self.main_widget = QWidget()
        self.setCentralWidget(self.main_widget)    # Set's the main_widget as the root widget

        layout = QVBoxLayout()  # Creates a vertical Layout to set the buttons in a vertical order

        # Main buttons
        btn_create = QPushButton("Create Database")
        btn_retrieve = QPushButton("Retrieve Database")
        btn_delete = QPushButton("Delete Database")
        btn_exit = QPushButton("Exit")

        btn_create.clicked.connect(self.create_database)
        btn_retrieve.clicked.connect(self.retrieve_database)
        btn_delete.clicked.connect(self.delete_database)
        btn_exit.clicked.connect(self.close)

        layout.addWidget(btn_create)
        layout.addWidget(btn_retrieve)
        layout.addWidget(btn_delete)
        layout.addWidget(btn_exit)

        self.main_widget.setLayout(layout)

    def create_database(self):
        CreateDatabaseDialog().exec_()   # This pops up a window, a dialog which is usually short lived and used as a form
        
    def retrieve_database(self):
        data = Write.readingFiles()
        if not data:
            QMessageBox.warning(self, "Error", "No databases found.")  # This shows a readymade dialog for any warning you encounter,
            return

        TableViewer(data).exec_()   # if no error TableViewer Dialog is opened, with data given as input
        

    def delete_database(self):
        data = Write.readingFiles()
        if not data:
            QMessageBox.warning(self, "Error", "No databases to delete.")
            return

        DeleteDatabaseDialog(data).exec_()  # Same thing as above


class CreateDatabaseDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Create Database")
        self.setGeometry(250, 250, 400, 300)

        layout = QVBoxLayout()

        self.name_input = QLineEdit()
        self.row_spin = QSpinBox()   # SpinBoxes are a special input for integers with arrows to increase or decrease
        self.col_spin = QSpinBox()

        self.row_spin.setMinimum(1)
        self.col_spin.setMinimum(1)

        form = QFormLayout()  # Simple form with the Line edits and QSpinBoxes appended, also gives them Labels
        form.addRow("Database Name:", self.name_input)
        form.addRow("Number of Rows:", self.row_spin)
        form.addRow("Number of Columns:", self.col_spin)
        layout.addLayout(form)

        save_btn = QPushButton("Save Database")
        save_btn.clicked.connect(self.save_database)
        layout.addWidget(save_btn)

        self.setLayout(layout)

    def save_database(self):
        nameDb = self.name_input.text().strip()
        intdbRow = self.row_spin.value()
        intdbColumn = self.col_spin.value()

        if not nameDb:
            QMessageBox.warning(self, "Error", "Please enter a database name.")
            return

        structured_columns = []
        for i in range(intdbColumn):
            col_name, ok = QInputDialog.getText(self, "Column Name", f"Column {i+1} name:")
            if not ok or not col_name.strip():
                return
            structured_columns.append(col_name.strip())

        structured_rows = []
        for i in range(intdbRow):
            row_data = {}
            for col in structured_columns:
                val, ok = QInputDialog.getText(self, "Row Data", f"Enter value for Row {i+1}, Column '{col}':")
                if not ok:
                    return
                row_data[col] = val
            structured_rows.append(row_data)

        TempDataList = {
            nameDb: {
                "columns": structured_columns,
                "rows": structured_rows
            }
        }
        Write.writingFiles(TempDataList)
        QMessageBox.information(self, "Success", f"Database '{nameDb}' created.")
        self.close()


class TableViewer(QDialog):
    def __init__(self, data):
        super().__init__()
        self.setWindowTitle("View Databases")
        self.setGeometry(250, 250, 600, 400)

        layout = QVBoxLayout()
        self.table = QTableWidget()
        layout.addWidget(self.table)

        if data:
            # Only display the first DB for simplicity
            for db_name, db_data in data.items():
                self.setWindowTitle(f"Viewing: {db_name}")
                self.table.setColumnCount(len(db_data["columns"]))
                self.table.setHorizontalHeaderLabels(db_data["columns"])
                self.table.setRowCount(len(db_data["rows"]))
                for i, row in enumerate(db_data["rows"]):
                    for j, col_name in enumerate(db_data["columns"]):
                        self.table.setItem(i, j, QTableWidgetItem(row[col_name]))
                break  # Remove this break if you want to display multiple DBs in a merged table

        self.setLayout(layout)


class DeleteDatabaseDialog(QDialog):
    def __init__(self, data):
        super().__init__()
        self.setWindowTitle("Delete Database")
        self.setGeometry(250, 250, 400, 300)

        layout = QVBoxLayout()
        self.data = data

        for db_name in data.keys():
            btn = QPushButton(f"Delete {db_name}")
            btn.clicked.connect(lambda _, name=db_name: self.delete_db(name))
            layout.addWidget(btn)

        self.setLayout(layout)

    def delete_db(self, name):
        with open("DataBase.json", "r") as file:
            db_data = json.load(file)

        if name in db_data:
            del db_data[name]
            with open("DataBase.json", "w") as file:
                json.dump(db_data, file, indent=4)
            QMessageBox.information(self, "Deleted", f"Database '{name}' deleted.")
            self.close()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = DatabaseManager()
    window.show()
    sys.exit(app.exec_())
