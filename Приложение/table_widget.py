from PyQt5.QtWidgets import QTableWidget, QTableWidgetItem
from PyQt5 import QtCore
class Table(QTableWidget):
    def __init__(self, wg, list_table, cur, con, t_name, rows):
        self.wg = wg  
        super().__init__(wg)
        self.tb_names = list_table
        self.cur = self.wg.cur
        self.con = con
        self.t_name = t_name
        self.setMinimumSize(QtCore.QSize(800, 500))
        self.verticalHeader().hide();
        self.updt(rows) # обновить таблицу
        self.setEditTriggers(QTableWidget.NoEditTriggers)
        self.cellClicked.connect(self.cellClick)  
# обновление таблицы
    def updt(self, rows):
        self.clear()
        self.setRowCount(0);
        self.t_name = self.wg.get_t_name()
        self.header = self.wg.list_tables_or_columns('c')
        self.setColumnCount(len(self.header))
        self.setHorizontalHeaderLabels(self.header)
        i = 0
        for elem in rows:
            self.setRowCount(self.rowCount() + 1)
            j = 0
            for t in elem: # заполняем внутри строки
                self.setItem(i, j, QTableWidgetItem(str(t).strip()))
                j += 1
            i += 1
        self.resizeColumnsToContents()
# обработка щелчка мыши по таблице
    def cellClick(self, row, col): 
        pk = []
        for c in range(len(self.wg.list_tables_or_columns('c'))):
            item = self.item(row, c).text()
            pk.append(item)
        self.wg.data = pk
        
        
        
        
        