import sys
import sqlite3

from PyQt5 import uic
from PyQt5.QtWidgets import QApplication, QMainWindow, QTableWidgetItem


class MyWidget(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('main.ui', self)
        self.connection = sqlite3.connect("coffee.sqlite")
        self.sp = ["Название сорта", "Тип прожарки", "Молотый/в зёрнах", "Описание вкуса", "Цена", "Объём упаковки"]
        self.run()

    def run(self):
        query = """SELECT name_of_sort, type_of_rare, [ground/grains], description_of_taste,
                   cost, size_of_packet FROM coffie"""
        res = self.connection.cursor().execute(query).fetchall()
        self.coffie_table.setColumnCount(6)
        self.coffie_table.setRowCount(0)
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

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MyWidget()
    ex.show()
    sys.exit(app.exec_())