import sys
import sqlite3

from PyQt5.QtWidgets import QApplication, QMainWindow, QTableWidgetItem, QWidget
from main_ui import Ui_MainWindow
from addEditCoffeeForm import Ui_Form


class MyWidget(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.connection = sqlite3.connect("data/coffee.sqlite")
        self.sp = ["Название сорта", "Тип прожарки", "Молотый/в зёрнах", "Описание вкуса", "Цена", "Объём упаковки"]
        self.run()
        self.reset.clicked.connect(self.run)
        self.add_change.clicked.connect(self.addEdit)

    def run(self):
        self.coffie_table.clear()
        query = """SELECT name_of_sort, type_of_rare, [ground/grains], description_of_taste,
                   cost, size_of_packet FROM coffie"""
        res = self.connection.cursor().execute(query).fetchall()
        self.coffie_table.setRowCount(0)
        self.coffie_table.setColumnCount(6)
        self.coffie_table.setHorizontalHeaderLabels(self.sp)
        for i, row in enumerate(res):
            self.coffie_table.setRowCount(self.coffie_table.rowCount() + 1)
            for j, elem in enumerate(row):
                if j == 2:
                    if elem:
                        self.coffie_table.setItem(i, j, QTableWidgetItem("Молотый"))
                    else:
                        self.coffie_table.setItem(i, j, QTableWidgetItem("В зёрнах"))
                else:
                    self.coffie_table.setItem(i, j, QTableWidgetItem(str(elem)))
        self.coffie_table.resizeColumnsToContents()
        self.coffie_table.verticalScrollBar().setSingleStep(10)
        self.coffie_table.horizontalScrollBar().setSingleStep(10)

    def addEdit(self):
        self.second_form = AddEdit()
        self.second_form.show()


class AddEdit(QWidget, Ui_Form):
    def __init__(self):
        super().__init__()
        self.connection = sqlite3.connect("data/coffee.sqlite")
        self.f = False
        self.make.clicked.connect(self.run)
        self.saving.clicked.connect(self.svng)

    def run(self):
        id = self.id.text()
        query = f"""SELECT name_of_sort, type_of_rare, [ground/grains], description_of_taste,
                           cost, size_of_packet FROM coffie WHERE id={id}"""
        res = self.connection.cursor().execute(query).fetchone()
        self.f = True
        if res == None:
            res = ('', '', '', '', '', '')
        self.sort.setText(res[0])
        self.type.setText(res[1])
        if res[2] == 0:
            self.molot_or_zerna.setText('В зёрнах')
        elif res[2] == 1:
            self.molot_or_zerna.setText('Молотый')
        self.taste.setText(res[3])
        self.cost.setText(str(res[4]))
        self.obem.setText(str(res[5]))

    def svng(self):
        name_of_sort, type_of_rare = self.sort.text(), self.type.text(),
        description_of_taste, cost, size_of_packet = self.taste.text(), self.cost.text(), self.obem.text()
        gg = 0 if self.molot_or_zerna.text() == 'В зёрнах' else 1
        if self.f:
            query = f"UPDATE coffie SET name_of_sort = '{name_of_sort}', type_of_rare = '{type_of_rare}'"
            query += f", [ground/grains] = {gg}, description_of_taste = '{description_of_taste}'"
            query += f", cost = {cost}, size_of_packet = {size_of_packet} WHERE id={self.id.text()}"
        else:
            query = "INSERT INTO coffie(id, name_of_sort, type_of_rare, [ground/grains], description_of_taste,"
            query += f"cost, size_of_packet) VALUES({self.id.text()}, '{name_of_sort}', '{type_of_rare}',"
            query += f" {gg}, '{description_of_taste}', {cost}, {size_of_packet})"
        self.connection.cursor().execute(query)
        self.connection.commit()
        self.close()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MyWidget()
    ex.show()
    sys.exit(app.exec_())
