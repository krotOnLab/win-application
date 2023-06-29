from PyQt5.QtGui import QKeySequence
from PyQt5.QtWidgets import (QListWidget, QShortcut, qApp,  QWidget)
import psycopg2
import pandas as pd
from table_widget import Table
from window_insert import ins_win
from window_edit import edit_win
from gui import Gui
from win_report import WinReport
from reports import Reports
class Form (QWidget):
    def __init__(self, login, password):
        super(Form, self).__init__()
        self.con(login, password)
        self.setMinimumWidth(1000)
        self.setMinimumHeight(600)
        self.setWindowTitle('Statistic')
        self.list_tables()
        self.gui = Gui(self)
        self.tb = Table(self, self.tb_names, self.cur, 
                        self.con, self.get_t_name(), self.update_table_rows('get rows') )
        if login == 'postgres':
            self.gui.administrator_layout()
        else:
            self.gui.manager_layout()
        # self.gui.manager_layout()
        self.mainLay.addWidget(self.tb, 0, 1, 11, 7)
        self.setLayout(self.mainLay)
        self.show()
        self.gui.center()
        self.shortcut_close = QShortcut(QKeySequence('Ctrl+Q'), self)
        self.shortcut_close.activated.connect(self.close_app)
        self.shortcut_open_insert_window = QShortcut(QKeySequence('Ctrl+I'), self)
        self.shortcut_open_insert_window.activated.connect(self.ins_w)
        self.shortcut_update = QShortcut(QKeySequence('Ctrl+U'), self)
        self.shortcut_update.activated.connect(self.upd)            
        self.data = []
        self.pk_old = []
    def close_app (self):
        self.con.close()
        self.close()
        qApp.quit()
# список таблиц    
    def list_tables (self):
        self.tb_names = QListWidget(self)
        tables = self.list_tables_or_columns(script =  't')
        try:
            tables.remove('Список_ФО')
        except:
            tables = tables
        self.tb_names.addItems(tables)
        self.tb_names.setCurrentRow(0)
        self.t_name = self.tb_names.item(self.tb_names.currentRow()).text()
        self.tb_names.clicked.connect(self.clicked)  
#обработчик клика по списку таблиц 
    def clicked(self, QModelIndex):
        self.t_name = self.tb_names.item(self.tb_names.currentRow()).text()
        return self.t_name 
# получение имени выбранной таблицы
    def get_t_name (self):
        t_name = self.tb_names.item(self.tb_names.currentRow()).text()
        return t_name
# получение значений выбранной таблицы
    def update_table_rows (self, key):
        operation = """SELECT  """
        for i in range (len(self.list_tables_or_columns('c'))):
            operation +=f"{self.cols[i]}, "
        operation = operation [:-2] +' '
        operation += f"""FROM {self.t_name}"""
        if key == 'get rows':
            self.cur.execute(operation)
            return self.cur.fetchall()
        else:
            self.upd(operation)
#получение списка имен таблиц или названий столбцов 
    def list_tables_or_columns(self, script):
        if script == 't':
            operation = """SELECT tablename FROM pg_catalog.pg_tables
            where schemaname = 'public'
            ORDER BY tablename ASC"""
            self.cur.execute(operation)
            operation = self.cur.fetchall()
            final_list = []
            for item in operation :
                final_list.append(item[0])  
            return final_list
        elif script == 'c':
            operation = f"""SELECT column_name FROM information_schema.columns
            WHERE 	table_name = '{self.t_name}'
            ORDER BY ordinal_position"""
            self.cur.execute(operation)
            self.table_columns = self.cur.fetchall()
            self.cols = ['ФО', 'Субъект_РФ', 'Год']
            for i in range(len(self.table_columns)-3):
                column = f"""SELECT column_name  AS c FROM information_schema.columns
            WHERE 	table_name = '{self.t_name}' AND 
                    column_name NOT IN ('{self.cols[0]}', '{self.cols[1]}', '{self.cols[2]}')
            ORDER BY ordinal_position LIMIT 1 OFFSET {i}"""
                self.cur.execute(column)
                col = self.cur.fetchall()
                self.cols.append(col[0][0])
            return self.cols
# соединение с базой данных
    def con(self, login, password):
        self.con = psycopg2.connect(user = login, 
                                    password =password,
                              host = "127.0.0.1", port = "5432", database = "Statistic")
        self.cur = self.con.cursor()
# обновить таблицу и поля
    def upd(self, query, key = 'update'):
        if key == 'update':
            self.cur.execute(query)
            self.con.commit()
            self.tb.updt(self.update_table_rows('get rows'))
        elif key == 'sort':
            self.cur.execute(query)
            rows = self.cur.fetchall()
            self.tb.updt(rows)
# открыть окно редактирования строки
    def edit_w(self):
        col = self.list_tables_or_columns('c')
        self.w_edit = edit_win(self, self.con, self.cur, col, self.data)
        self.w_edit.show()  
        for i in range(3):self.pk_old.append(self.data[i])
# Редкатирование строки и внесение изменений 
    def edit (self):
        pk = self.pk_old
        cols = self.list_tables_or_columns('c')
        query = f'UPDATE {self.t_name} SET '
        for i in range(len(self.data)):
            try :   value = float(self.data[i])
            except ValueError : continue
            if type(value)==str:
                query+=f"'{cols[i]} = {value}', "
            if type(value)==float:
                query+=f'{cols[i]} = {value}, '
        query = query [:-2] + f""" WHERE ФО = '{pk[0]}' 
                                AND Субъект_РФ = '{pk[1]}' AND Год = {pk[2]} """
        self.pk_old.clear()
        self.upd(query)
 # добавить в таблицу новую строку       
    def insert (self):
        cols = self.list_tables_or_columns('c')
        query = f'INSERT INTO {self.t_name} ('
        for i in range(len(cols)):
            query +=f'{cols[i]}, '
        query = query[:-2] + ') VALUES\n('
        for col in self.data:
            try :   col = float(col)
            except ValueError : continue
            if type(col)==str:
                query+=f"'{col}', "
            if type(col)==float:
                query+=f'{col}, '
        query = query [:-2] +')'
        self.upd(query)    
# открыть окно для добавления строки в таблицу
    def ins_w(self):
        col = self.list_tables_or_columns('c')
        self.w_ins = ins_win(self, self.t_name, self.con, self.cur, col)
        self.w_ins.show()
# удалить из таблицы строку
    def dels(self):
        query = f"""DELETE FROM {self.t_name} 
        WHERE ФО = '{self.data[0]}' AND Субъект_РФ =  '{self.data[1]}' 
                                    AND Год = '{int(self.data[2])}'"""
        self.upd(query)
# создание выбранного отчета
    def selected_report (self, report, lists, years, parameters ):
        df = pd.DataFrame(self.update_table_rows('get rows'), columns = self.cols)
        if report == 'Структура показателя\nна уровне ФО': 
            Reports.pie_F(df, lists, years, parameters)
        elif report == 'Субъекты РФ и\nстат.показатели': 
            Reports.list_FO(df, lists, years, parameters)
        elif report == 'Рейтинг субъектов РФ\nв рамках ФО и года':
            Reports.rating_per_param(df, lists, years, parameters)
        elif report == 'Рейтинг субъектов РФ\nв рамках года': 
            Reports.rating(df, lists[0], years, parameters)
        elif report == 'Стат.показатели с динамикой': 
            Reports.list_and_dynamic_plot(df, lists[0], years, parameters)
    def win_rep (self):
        self.win_reports = WinReport(self, self.update_table_rows('get rows'), 
                                     self.list_tables_or_columns('c'))
    def sort (self):
        operation = 'SELECT '
        for column in self.list_tables_or_columns('c'):
            operation += f'{column}, '
        operation = operation[:-2]
        operation += f" FROM {self.t_name}"
        if self.box_sort.currentText() == 'По возрастанию':
            operation +='\nORDER BY ФО ASC, Субъект_РФ ASC, Год ASC'
        elif self.box_sort.currentText() == 'По убыванию':
            operation +='\nORDER BY ФО DESC, Субъект_РФ DESC, Год DESC'
        elif self.box_sort.currentText() == 'Специальная':
            fd_list = ['Центральный федеральный округ', 'Северо-Западный федеральный округ', 
                       'Южный федеральный округ', 'Северо-Кавказский федеральный округ',
                       'Приволжский федеральный округ', 'Уральский федеральный округ',
                       'Сибирский федеральный округ','Дальневосточный федеральный округ']
            operation = 'SELECT '
            for column in self.list_tables_or_columns('c'):
                operation += f'{column}, '
            operation = operation[:-2] + ' FROM ('
            for fd in fd_list:
                operation += '\n(SELECT '
                for column in self.list_tables_or_columns('c'):
                    operation += f'{column}, '
                operation = operation[:-2] + f" FROM {self.t_name}\nWHERE ФО = '{fd}') UNION"
            operation = operation[:-6] + ')as tbl ORDER BY CASE'
            for i, fd in enumerate(fd_list):
                operation+=f"\nWHEN ФО = '{fd}' then {i}"
            operation +=' END, Год ASC, Субъект_РФ ASC '
        self.upd(operation, key = 'sort')
    
