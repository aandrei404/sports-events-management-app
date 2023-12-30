from PyQt6.QtWidgets import QWidget
from PyQt6.QtSql import QSqlDatabase, QSqlQuery
from PyQt6 import QtTest

from package.mainWindow import MainWindow

# needed for the GUI design
from package.ui.login_ui import Ui_FormLogIn


class LoginWindow(QWidget):
    def __init__(self):
        super().__init__()

        # setup the GUI
        self.ui = Ui_FormLogIn()
        self.ui.setupUi(self)

        # login button logic
        self.ui.logInButton.clicked.connect(self.checkCredential)

        # connect to the database where user info is stored
        self.connectLoginDb()

    # sqlite connection to the database
    def connectLoginDb(self):
        self.loginDb = QSqlDatabase.addDatabase("QSQLITE", "login")
        self.loginDb.setDatabaseName(".\\db\\userInfo.sqlite")

        if not self.loginDb.open():
            self.ui.labelStatus.setText("Connection failed")

    # login logic
    def checkCredential(self):
        username = self.ui.lineEditUsername.text()
        password = self.ui.lineEditPassword.text()

        # I know this is not safe, will change in the future
        query = QSqlQuery(self.loginDb)
        query.prepare("SELECT * FROM userInfo WHERE Username=:username")
        query.bindValue(":username", username)
        query.exec()

        # if we find the username
        if query.first():
            # check the password and login if it matches
            if query.value("Password") == password:
                self.ui.labelStatus.setText("Logged in")

                QtTest.QTest.qWait(200)

                # start the main app window
                self.app = MainWindow()
                self.app.show()

                self.loginDb.close()
                self.close()
            else:
                self.ui.labelStatus.setText(
                    "Password is incorrect"
                )  # if not, inform the user about the password
        else:
            self.ui.labelStatus.setText(
                "Username is not found"
            )  # if not, inform the user about the username
