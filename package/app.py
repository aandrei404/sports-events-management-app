import sys
import sys
from PyQt6.QtWidgets import QWidget, QApplication, QPushButton, QFrame, QMessageBox, QTableWidgetItem, QSizePolicy
from PyQt6.QtCore import pyqtSlot
from PyQt6.QtGui import QIntValidator
from PyQt6.QtSql import QSqlDatabase, QSqlQuery, QSqlQueryModel
from PyQt6.QtWidgets import QGridLayout, QLabel, QLineEdit
from PyQt6 import QtTest

from package.loginWindow import LoginWindow

def run():
    app = QApplication(sys.argv)
    
    loginWindow = LoginWindow()
    loginWindow.show()

    sys.exit(app.exec())