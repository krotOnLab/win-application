
from PyQt5.QtWidgets import (QPushButton, QComboBox, QLabel,
                            QDesktopWidget, qApp, QGridLayout, QWidget)
class Gui (QWidget):
    def __init__(self, mw):
        super(Gui, self).__init__()
        self.mw = mw
# кнопка "обновить"
    def update_button (self):
        self.mw.btn_up = QPushButton('Обновить', self)
        self.mw.btn_up.clicked.connect(self.mw.update_table_rows)
# кнопка "Редактировать"
    def edit_button (self):
        self.mw.btn_edit = QPushButton('Редактировать', self)
        self.mw.btn_edit.clicked.connect(self.mw.edit_w)
# кнопка добавить запись
    def insert_button (self):
        self.mw.btn_ins = QPushButton('Добавить', self)
        self.mw.btn_ins.clicked.connect(self.mw.ins_w)
# кнопка удалить запись
    def delete_button (self):
        self.mw.btn_del = QPushButton('Удалить', self)
        self.mw.btn_del.clicked.connect(self.mw.dels)
# кнопка закрыть приложение       
    def close_button (self):
        self.mw.btn_cl = QPushButton('Закрыть', self)
        self.mw.btn_cl.clicked.connect(self.mw.con.close)   
        self.mw.btn_cl.clicked.connect(self.mw.close)
        self.mw.btn_cl.clicked.connect(qApp.quit)
# список вилов сортировок
    def sort (self):
        self.mw.box_sort = QComboBox()
        self.mw.box_sort.addItems(['По возрастанию', 
                                   'По убыванию', 'Специальная'])
        self.mw.btn_sort = QPushButton('Сортировать')
        self.mw.btn_sort.clicked.connect(self.mw.sort)
        self.mw.l_sort = QLabel('Виды сортировок')                
#центрирование окна
    def center (self):
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())        
# макет для пользователя со всеми правами и привелегиями
    def administrator_layout (self):
        self.mw.mainLay = QGridLayout()
        self.mw.mainLay.setSpacing(10)
        self.mw.setLayout(self.mw.mainLay)
        self.update_button()
        self.edit_button()
        self.insert_button()
        self.delete_button()
        self.sort()
        self.mw.btn_rep = QPushButton('Отчеты')
        self.mw.btn_rep.clicked.connect(self.mw.win_rep)
        self.mw.mainLay.addWidget(self.mw.tb_names, 0, 0, 1, 1)
        self.mw.mainLay.addWidget(self.mw.btn_up,   3, 0, 1, 1)
        self.mw.mainLay.addWidget(self.mw.btn_edit, 4, 0, 1, 1)
        self.mw.mainLay.addWidget(self.mw.btn_ins,  5, 0, 1, 1)
        self.mw.mainLay.addWidget(self.mw.btn_del,  6, 0, 1, 1)
        self.mw.mainLay.addWidget(self.mw.l_sort,   7, 0, 1, 1)
        self.mw.mainLay.addWidget(self.mw.box_sort, 8, 0, 1, 1)
        self.mw.mainLay.addWidget(self.mw.btn_sort, 9, 0, 1, 1)
        self.mw.mainLay.setColumnMinimumWidth(0, 300)
        self.mw.mainLay.setRowMinimumHeight(0, 300)
        self.mw.mainLay.setColumnStretch(1, 2)
        self.mw.mainLay.setRowStretch(0, 0)
# макет для пользователя с правами на получение данных из таблиц и построение отчетов
    def manager_layout (self):
        self.mw.mainLay = QGridLayout()
        self.mw.mainLay.setSpacing(10)
        self.mw.setLayout(self.mw.mainLay)
        self.update_button()
        self.sort()
        self.mw.btn_rep = QPushButton('Отчеты')
        self.mw.btn_rep.clicked.connect(self.mw.win_rep)
        self.mw.mainLay.addWidget(self.mw.tb_names, 0, 0, 1, 1)
        self.mw.mainLay.addWidget(self.mw.btn_up, 4, 0, 1, 1)
        self.mw.mainLay.addWidget(self.mw.btn_rep, 5, 0, 1, 1)
        self.mw.mainLay.addWidget(self.mw.l_sort,   6, 0, 1, 1)
        self.mw.mainLay.addWidget(self.mw.box_sort, 7, 0, 1, 1)
        self.mw.mainLay.addWidget(self.mw.btn_sort, 8, 0, 1, 1)
        self.mw.mainLay.setColumnMinimumWidth(0, 300)
        self.mw.mainLay.setRowMinimumHeight(0, 300)
        self.mw.mainLay.setColumnStretch(1, 2)
        self.mw.mainLay.setRowStretch(0, 0)