from PyQt5.QtWidgets import (QWidget,QLabel, QLineEdit,
                             QPushButton, QGridLayout)
from PyQt5.QtCore import Qt
class ins_win (QWidget):
    def __init__(self, mw, t_name, con,  cur, col):
        super(ins_win, self).__init__()
        self.setWindowTitle('Значение для добавления в таблицу')
        self.setMinimumWidth(200)
        self.setMinimumHeight(200)
        self.t_name = t_name
        self.con = con
        self.cur =cur
        self.mw =mw
        self.col = col
        self.value_ins =[]
        self.gui(self.col)
#  графический интерфейс 
    def gui(self, col):
        self.lay = QGridLayout(self)
        for i in range(len(col)):
            self.l = QLabel(self, text = self.col[i])
            self.lay.addWidget(self.l, 0, i, 1, 1, Qt.AlignJustify)
        for i in range(len(col)):
            self.el = QLineEdit(self)
            self.lay.addWidget(self.el, 1, i, 1, 1,  Qt.AlignJustify)
        self.btn = QPushButton(self)
        self.btn.setText("Добавить значения")
        self.btn.clicked.connect(self.btn_ins)
        self.lay.addWidget(self.btn, 2, 0, 1, len(col),Qt.AlignCenter )
#  обработчик нажития кнопки добавления значения
    def btn_ins (self):
        value_ins = []
        for i in range(len(self.col)):
            item = self.lay.itemAtPosition(1, i).widget()
            if isinstance(item, QLineEdit):
                value_ins.append(item.text())
        self.mw.data = value_ins
        self.close()
        self.mw.insert()

