
from PyQt5.QtGui import *
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import (QPushButton, QListWidget,QLabel, 
                             QGridLayout, QWidget, QAbstractItemView, QMessageBox)
from PyQt5.Qt import (QMargins)
import pandas as pd
class WinReport(QWidget):
    def __init__(self, mw, data, name_columns):
        super(WinReport, self).__init__()
        self.setWindowTitle('Мастер создания отчета')
        self.setMinimumWidth(400)
        self.setMinimumHeight(200)
        self.mw = mw
        self.rows = pd.DataFrame(data, columns=name_columns)
        self.gui()
        self.mw.gui.center() 
        self.show()
        self.report_name = []
        self.list_selected_param = []
        self.list_selected_regions = []
        self.list_selected_years = []  
        self.list_selected_fd = []
        self.key = 'r' 
# Внешний вид окна 
    def gui(self):
        self.grid = QGridLayout()
        self.list_reports = QListWidget()
        self.list_reports.itemClicked.connect(self.select_report) 
        self.label_g = QLabel('Выберите вид отчета', self)
        self.label_r = QLabel('В рамках чего хотите отчет?', self)
        self.list_regions = QListWidget(self)
        self.list_regions.addItems(['Федеральные округа', 'Регионы', 'Регионы в рамках\nфедерального округа'])
        self.list_regions.itemSelectionChanged.connect(self.select_list_type_regions)
        self.btn_ok = QPushButton('Сделать отчет')
        self.btn_ok.clicked.connect(self.create_report)
        self.label_l = QLabel('Выберите значения из списка', self)
        self.list = QListWidget(self)
        self.list.setSelectionMode(QAbstractItemView.ExtendedSelection)
        self.list.itemSelectionChanged.connect(self.selected_regions)
        self.label_year_1 = QLabel('Выберите')
        self.label_year_2 = QLabel('интересующие года')
        self.list_years = QListWidget(self)
        self.list_years.addItems([str(year) for year in self.rows['Год'].sort_values().unique()])
        self.list_years.setSelectionMode(QAbstractItemView.ExtendedSelection)
        self.list_years.itemSelectionChanged.connect(self.selected_years)
        self.label_param = QLabel('Выберите показатели')
        self.list_param = QListWidget(self)
        self.grid.addWidget(self.label_g,       4, 0, 1, 1, Qt.AlignCenter)
        self.grid.addWidget(self.list_reports,  5, 0, 2, 1)
        self.grid.addWidget(self.label_r,       0, 0, 2, 1, Qt.AlignCenter)
        self.grid.addWidget(self.list_regions,  2, 0, 2, 1)
        self.grid.addWidget(self.label_param,   7, 0, 1, 1, Qt.AlignCenter)
        self.grid.addWidget(self.list_param,    8, 0, 2, 1)
        self.grid.addWidget(self.btn_ok,        10, 0, 1, 1)
        self.grid.addWidget(self.label_l,   0, 1, 2, 1, Qt.AlignCenter)
        self.grid.addWidget(self.list,      2, 1, 8, 1)
        self.grid.setRowMinimumHeight(5, 250)
        self.grid.setColumnMinimumWidth(1, 400)
        self.grid.setColumnMinimumWidth(0, 300)
        self.grid.addWidget(self.label_year_1, 0, 2, 1, 1, Qt.AlignCenter)
        self.grid.addWidget(self.label_year_2, 1, 2, 1, 1, Qt.AlignCenter)
        self.grid.addWidget(self.list_years, 2, 2, 8, 1)
        self.list_param.addItems([year for year in self.rows.columns if year not in ('ФО', 'Субъект_РФ', 'Год')])
        self.list_param.setSelectionMode(QAbstractItemView.ExtendedSelection)
        self.list_param.itemSelectionChanged.connect(self.selected_param)
        self.setLayout(self.grid)
        self.grid.setContentsMargins(QMargins(20, 20, 20, 20))
        self.grid.setVerticalSpacing(10)
        self.setFont(QFont('Arial', 12))
#  Выбор режима отбора субъектов для отчета 
    def select_list_type_regions(self):
        list_type_regions = self.list_regions.item(self.list_regions.currentRow()).text()
        if list_type_regions == 'Федеральные округа':
            self.insert_federal_district()
            self.key = 'fd'
            self.insert_reports()
        elif list_type_regions == 'Регионы':
            self.insert_regions()
            self.key = 'r'
            self.insert_reports()
        elif list_type_regions == 'Регионы в рамках\nфедерального округа':
            self.insert_federal_district_and_regions()
            self.key = 'fd-r'
            self.insert_reports()
# Выбор отчета      
    def select_report(self):
        self.report_name = self.list_reports.item(self.list_reports.currentRow()).text()
        print(self.report_name)
# Вставка списка федеральных округов 
    def insert_federal_district (self):
        self.list.clear()
        fd_list = self.rows['ФО'].sort_values().unique()
        self.list.addItems(fd_list)
        self.key = 'fd'
# Вставка списка регионов 
    def insert_regions (self):
        self.list.clear()
        regions = self.rows['Субъект_РФ'].sort_values().unique()
        self.list.addItems(regions)
        self.key = 'r'
# Вставка смешанного списка 
    def insert_federal_district_and_regions (self):
        self.list.clear()
        fd_list = ['Центральный федеральный округ', 'Северо-Западный федеральный округ', 
                   'Южный федеральный округ', 'Северо-Кавказский федеральный округ',
                   'Приволжский федеральный округ', 'Уральский федеральный округ',
                   'Сибирский федеральный округ','Дальневосточный федеральный округ']
        for fd in fd_list:
            fd_regions = self.rows['Субъект_РФ'].loc[self.rows['ФО'].isin([fd])].sort_values().unique()
            self.list.addItem(fd)
            self.list.setCurrentRow(self.list.count())
            font = QFont()
            font.setBold(True)
            self.list.item(self.list.count()-1).setFont(font)
            self.list.addItems(fd_regions)
        self.key = 'fd-r'
# Создание списка отчетов        
    def insert_reports (self):
        self.list_reports.clear()
        if self.key == 'r':
            self.list_reports.addItems(
                ['Рейтинг субъектов РФ\nв рамках года', 
                 'Стат.показатели с динамикой'])
        elif self.key == 'fd':
            self.list_reports.addItems(
                ['Структура показателя\nна уровне ФО',
                 'Субъекты РФ и\nстат.показатели',
                 'Рейтинг субъектов РФ\nв рамках ФО и года'])
        elif self.key == 'fd-r':
            self.list_reports.addItems(
                ['Структура показателя\nна уровне ФО', 
                 'Субъекты РФ и\nстат.показатели',
                 'Рейтинг субъектов РФ\nв рамках ФО и года'])   
#обработчик клика по списку таблиц 
    def selected_regions(self):
        temp = []
        if self.key == 'r':
            items = self.list.selectedItems()
            for item in items:
                temp.append(item.text())
            print(temp)
            self.list_selected_regions = temp  
        if self.key == 'fd':
            items = self.list.selectedItems()
            for item in items:
                temp.append(item.text())
            print(temp)
            self.list_selected_fd = temp  
        if self.key == 'fd-r':
            fds = []
            items = self.list.selectedItems()
            fd = self.rows['ФО'].unique()
            # print(fd)
            for item in items:
                if item.text() in fd:
                    fds.append(item.text())
                else:
                    temp.append(item.text())
            print(temp)
            print(fds)
            self.list_selected_regions = temp 
            self.list_selected_fd = fds
#обработчик выбора из списка годов 
    def selected_years(self):
        temp = []
        items = self.list_years.selectedItems()
        for item in items:
            temp.append(int(item.text()))
        print(temp)
        self.list_selected_years = temp
# обработчик выбора из списка статистических показателей 
    def selected_param (self):
        temp = []
        items = self.list_param.selectedItems()
        for item in items:
            temp.append(item.text())
        print(temp)
        self.list_selected_param = temp
# обработчик клика по кнопке "Сделать отчет" 
    def create_report (self):
        if self.condition() :
            self.mw.selected_report(self.report_name, 
                                    [self.list_selected_regions,self.list_selected_fd], 
                                    self.list_selected_years, self.list_selected_param )
        else:
            QMessageBox.about(self, 'Выбраны не все поля',
                              'Выберите все поля, чтобы сформировать отчет')
# Проверка, что все поля выбраны 
    def condition (self):
        if self.key == 'r': 
            if ((len(self.report_name) != 0) and 
                (len(self.list_selected_years) != 0 )and 
                (len(self.list_selected_param) !=0) and 
                (len(self.list_selected_regions) != 0)):
                return True
            else :
                return False
        if self.key == 'fd':
            if ((len(self.report_name) != 0) and 
                (len(self.list_selected_years) != 0 ) and
                (len(self.list_selected_param) !=0) and
                (len(self.list_selected_fd) != 0)):
                return True
            else :
                return False
        if self.key == 'fd-r':
            if ((len(self.report_name) != 0) and
                (len(self.list_selected_years) != 0 )and
                (len(self.list_selected_param) !=0) and
                ((len(self.list_selected_regions) != 0) and
                (len(self.list_selected_fd) != 0))):
                return True
            else :
                return False
            
        
        
