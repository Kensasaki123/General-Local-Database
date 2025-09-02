import sys
import json
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QPushButton,
    QLineEdit, QSpinBox, QTableWidget, QTableWidgetItem,
    QMessageBox, QFormLayout, QDialog, QInputDialog, QLabel
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
        btn_modify = QPushButton("Modify Database")
        btn_retrieve = QPushButton("Retrieve Database")
        btn_delete = QPushButton("Delete Database")
        btn_exit = QPushButton("Exit")

        btn_create.clicked.connect(self.create_database)
        btn_modify.clicked.connect(self.modify_database)
        btn_retrieve.clicked.connect(self.retrieve_database)
        btn_delete.clicked.connect(self.delete_database)
        btn_exit.clicked.connect(self.close)

        layout.addWidget(btn_create)
        layout.addWidget(btn_modify)
        layout.addWidget(btn_retrieve)
        layout.addWidget(btn_delete)
        layout.addWidget(btn_exit)

        self.main_widget.setLayout(layout)

    def create_database(self):
        CreateDatabaseDialog().exec_()   # This pops up a window, a dialog which is usually short lived and used as a form

        # An imp note about this is that it comes with a question mark "?" to maybe add a help button so YEah, it's a default thingy.
        
    def modify_database(self):
        ModifyDatabaseDialog().exec_()


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

class ModifyDatabaseDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Modify Database")
        self.setGeometry(250, 250, 400, 300)
        self.main_layout = QVBoxLayout()
        
        btn_rename = QPushButton("Rename Elements")
        btn_ChangeRow = QPushButton("Change Row/Columns")


        self.main_layout.addWidget(btn_rename)
        self.main_layout.addWidget(btn_ChangeRow)

        self.setLayout(self.main_layout)

        btn_rename.clicked.connect(self.handleRename)
        btn_ChangeRow.clicked.connect(self.handleChangeRow)
 
    def handleRename(self):
        self.close()
        rename_dialog = RenameDialog()
        rename_dialog.exec_() 

    def handleChangeRow(self):
        self.close()
        ChangeRow_dialog = ChangeRowDialog()
        ChangeRow_dialog.exec_() 

class ChangeRowDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Change Row/Columns")
        self.setGeometry(300, 300, 800, 800)

        self.layout2 = QVBoxLayout()
        
 
 
class RenameDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Rename Database/Elements")
        self.setGeometry(300, 300, 800, 800)

        self.layout1 = QVBoxLayout()

        
        raw_data = Write.readingFiles()
        self.db_names = list(raw_data.keys())   # store db names
        self.open_containers = {}  
        for i, names in enumerate(self.db_names):
            btn = QPushButton(names)
            btn.clicked.connect(lambda _, idx=i: self.renameFunc(idx))

            self.layout1.addWidget(btn)

        self.setLayout(self.layout1)
                
    
    def renameFunc(self, i):
        container = QWidget()
        container_layout = QVBoxLayout(container)

        read_data = Write.readingFiles()  # refresh data
        db_name = self.db_names[i]
        database_data = read_data[db_name]

        close_btn = QPushButton(f"Close {db_name}")
        container_layout.addWidget(close_btn)

        Changes_btn = QPushButton(f"Confirm Changes")
        container_layout.addWidget(Changes_btn)

        table = QTableWidget()
        container_layout.addWidget(table)

        # Fill the table
        table.clear()
        table.setColumnCount(len(database_data["columns"]))
        table.setHorizontalHeaderLabels(database_data["columns"])
        table.setRowCount(len(database_data["rows"]))

        for i, row in enumerate(database_data["rows"]):
            for j, col_name in enumerate(database_data["columns"]):
                # ensure the stored value is a string (QTableWidgetItem expects str)
                val = row.get(col_name, "")
                table.setItem(i, j, QTableWidgetItem(str(val)))

        # add to main layout and remember the container
        self.layout1.addWidget(container)
        Changes_btn.clicked.connect(lambda _, t=table, name=db_name: self.ButtonHandle(t, name))

        self.open_containers[db_name] = container

        # connect close button to a helper that knows which container/db to close
        close_btn.clicked.connect(lambda _, c=container, name=db_name: self._close_container(c, name))

    def ButtonHandle(self, table, db_name):
        all_data = Write.readingFiles()
        db_data = all_data[db_name]

        for row_idx in range(table.rowCount()):
            for col_idx, col_name in enumerate(db_data["columns"]):
                item = table.item(row_idx, col_idx)
                val = item.text() if item else ""
                db_data["rows"][row_idx][col_name] = val
        
        all_data[db_name] = db_data
        Write.writingFiles(all_data)

    def handleItem_change(self, item):
        pass    
    
    def _close_container(self, container, db_name):
        # defensive: only act if container is actually present
        if db_name in self.open_containers:
            try:
                # remove from layout and delete widget
                self.layout1.removeWidget(container)
                container.setParent(None)    # detach from Qt parent
                container.deleteLater()
            finally:
                # always clear the record so the DB can be opened again
                self.open_containers.pop(db_name, None)


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
        # These three variables take in the values from out LineEdit.
        nameDb = self.name_input.text().strip()
        intdbRow = self.row_spin.value()
        intdbColumn = self.col_spin.value()

        # A warning sign which triggers if no name is found, cuz the row and column input already have default values.
        if not nameDb:
            QMessageBox.warning(self, "Error", "Please enter a database name.")
            return

        structured_columns = []
        for i in range(intdbColumn):
            col_name, ok = QInputDialog.getText(self, "Column Name", f"Column {i+1} name:") # QInputDialog creates a small pop-up for inputs Here it returns the name col_name var and also returns boolean ok.
            if not ok or not col_name.strip():  # If either of the situatuin is true, the code will return back
                return
            structured_columns.append(col_name.strip()) # If not then it appends the stripped data

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
        self.setGeometry(250, 250, 800, 600)

        self.main_layout = QVBoxLayout()
        self.setLayout(self.main_layout)

        # list of database names
        self.db_names = list(data.keys())

        # map open database name -> its container widget (so we can close it reliably)
        self.open_containers = {}

        # create buttons that open DB views
        for i, name in enumerate(self.db_names):
            btn = QPushButton(name)
            btn.clicked.connect(lambda _, idx=i: self.button_handle(idx))
            self.main_layout.addWidget(btn)

    def button_handle(self, idx):
        read_data = Write.readingFiles()  # refresh data
        db_name = self.db_names[idx]
        database_data = read_data[db_name]

        # Prevent opening the same DB multiple times (use db_name as the key)
        if db_name in self.open_containers:
            return

        # Container holds the close button + table
        container = QWidget()
        container_layout = QVBoxLayout(container)

        close_btn = QPushButton(f"Close {db_name}")
        container_layout.addWidget(close_btn)

        table = QTableWidget()
        container_layout.addWidget(table)

        # Fill the table
        table.clear()
        table.setColumnCount(len(database_data["columns"]))
        table.setHorizontalHeaderLabels(database_data["columns"])
        table.setRowCount(len(database_data["rows"]))

        for i, row in enumerate(database_data["rows"]):
            for j, col_name in enumerate(database_data["columns"]):
                # ensure the stored value is a string (QTableWidgetItem expects str)
                val = row.get(col_name, "")
                table.setItem(i, j, QTableWidgetItem(str(val)))

        # add to main layout and remember the container
        self.main_layout.addWidget(container)
        self.open_containers[db_name] = container

        # connect close button to a helper that knows which container/db to close
        close_btn.clicked.connect(lambda _, c=container, name=db_name: self._close_container(c, name))

    def _close_container(self, container, db_name):
        # defensive: only act if container is actually present
        if db_name in self.open_containers:
            try:
                # remove from layout and delete widget
                self.main_layout.removeWidget(container)
                container.setParent(None)    # detach from Qt parent
                container.deleteLater()
            finally:
                # always clear the record so the DB can be opened again
                self.open_containers.pop(db_name, None)


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
