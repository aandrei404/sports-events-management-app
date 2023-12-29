import sys
from PyQt6.QtWidgets import QWidget, QApplication, QPushButton, QFrame, QMessageBox, QTableWidgetItem, QSizePolicy
from PyQt6.QtCore import pyqtSlot
from PyQt6.QtGui import QIntValidator
from PyQt6.QtSql import QSqlDatabase, QSqlQuery, QSqlQueryModel
from PyQt6.QtWidgets import QGridLayout, QLabel, QLineEdit
from PyQt6 import QtTest

from package.mainWindow import MainWindow

from package.ui.login_ui import Ui_FormLogIn

class LoginWindow(QWidget):
    def __init__(self):
        super().__init__()
        
        self.ui = Ui_FormLogIn()
        self.ui.setupUi(self)
        
        self.ui.logInButton.clicked.connect(self.checkCredential)

        self.connectLoginDb()
        
    def connectLoginDb(self):
        self.loginDb = QSqlDatabase.addDatabase('QSQLITE', 'login')
        self.loginDb.setDatabaseName('.\\data\\userInfo.sqlite')
    
        if not self.loginDb.open():
            self.ui.labelStatus.setText('Connection failed')

    def checkCredential(self):
        username = self.ui.lineEditUsername.text()
        password = self.ui.lineEditPassword.text()
    
        query = QSqlQuery(self.loginDb)
        query.prepare('SELECT * FROM userInfo WHERE Username=:username')
        query.bindValue(':username', username)
        query.exec()
    
        if query.first():
            if query.value('Password') == password:
                self.ui.labelStatus.setText('Logged in')

                QtTest.QTest.qWait(200)
            
                self.app = MainWindow()
                self.app.show()
            
                self.loginDb.close()
                self.close()
            else:
                self.ui.labelStatus.setText('Password is incorrect')
        else:
            self.ui.labelStatus.setText('Username is not found')