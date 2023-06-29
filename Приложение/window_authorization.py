
from PyQt5.QtWidgets import (QPushButton, qApp,  QGridLayout, QWidget,
                             QLineEdit, QLabel,QMessageBox)
from PyQt5.QtGui import QFont
from PyQt5.QtCore import Qt
from main_window import Form
class authorization (QWidget):
    def __init__(self ):
        super(authorization, self).__init__()
        self.setWindowTitle('Авторизация')
        self.setMinimumWidth(200)
        self.setMinimumHeight(200)
        self.layout = QGridLayout()
        self.setLayout(self.layout)
        self.gui()
   
    def gui (self):
        self.font = QFont('TimesNewRoman', 10)
        annotation = QLabel('Введите логин и пароль для доступа к базе данных')
        annotation.setFont(self.font)
        login_label = QLabel('Логин')
        login_label.setFont(self.font)
        password_label = QLabel('Пароль')
        password_label.setFont(self.font)
        self.login = QLineEdit()
        self.password = QLineEdit()
        enter = QPushButton('Войти')
        cancel = QPushButton('Отмена')
        enter.setMinimumWidth(150)
        cancel.setMinimumWidth(150)
        self.layout.addWidget(annotation, 0, 0, 1, 2,  Qt.AlignCenter)
        self.layout.addWidget(login_label, 1, 0, 1, 1, Qt.AlignCenter)
        self.layout.addWidget(self.login, 1, 1, 1, 1)
        self.layout.addWidget(password_label, 2, 0, 1, 1, Qt.AlignCenter)
        self.layout.addWidget(self.password, 2, 1, 1, 1)
        self.layout.addWidget(enter, 3, 0, 1, 1)
        self.layout.addWidget(cancel, 3, 1, 1, 1, Qt.AlignCenter)
        self.layout.setVerticalSpacing(30)
        cancel.clicked.connect(self.close)
        cancel.clicked.connect(qApp.quit)
        enter.clicked.connect(self.enter_btn)
    def enter_btn (self):
        print('!-')
        users = {'postgres':'passwfordb', 'viewer':'manager'}
        login = self.login.text()
        password = self.password.text()
        flag = False
        for log, pas in users.items():
            print(f'log: {log}, pas:{pas}, login:{login}, password:{password}')
            if log == login and pas == password:
                flag = True
                self.close()
                Form (login, password)
        if flag == False:
            msg = QMessageBox()
            msg.setWindowTitle('Ошибка')
            msg.setText('Неправильно введем логин и/или пароль')
            msg.setStandardButtons(QMessageBox.Ok)
            msg.setEscapeButton(QMessageBox.Ok)
            msg.exec_()
                     
