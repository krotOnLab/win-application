from PyQt5.QtWidgets import (QWidget, QLabel, QLineEdit, 
                             QPushButton, QGridLayout)
from PyQt5.QtCore import Qt
class edit_win (QWidget):
    def __init__(self, mw, con,  cur, cols, data):
        super(edit_win, self).__init__()
        self.setWindowTitle('Редактировать запись')
        self.setMinimumWidth(200)
        self.setMinimumHeight(200)
        self.mw =mw
        self.con = con
        self.cur =cur
        self.cols = cols
        self.values = data
        self.value_edit =[]
        self.gui(self.cols, self.values)
#  графический интерфейс 
    def gui (self, cols, values):
        self.lay = QGridLayout(self)
        for i, col in enumerate(cols):
            self.l = QLabel(self, text = col )
            self.lay.addWidget(self.l, 0, i, 1, 1)
            self.lay.setColumnMinimumWidth(i, 300)
        for i in range(len(values)):
            self.el = QLineEdit(self)
            self.el.setText(values[i])
            self.lay.addWidget(self.el, 1, i, 1, 1)
        self.btn = QPushButton(self)
        self.btn.setText("Применить изменения")
        self.btn.clicked.connect(self.btn_edit)
        self.lay.addWidget(self.btn, 2, 0, 1, len(values), Qt.AlignCenter)
#  обработчик нажатия кнопки редактировать
    def btn_edit (self):
        value_edit = []
        pk_old = []
        pk_number=0
        for i in range(len(self.cols)):
            
            item = self.lay.itemAtPosition(1, i).widget()
            if isinstance(item, QLineEdit):
                value_edit.append(item.text())
                if pk_number == 3 : continue
                else: pk_old.append(item.text())
            pk_number+=1
        self.mw.data = value_edit
        self.mw.pk_pld = pk_old
        self.close()
        self.mw.edit()

