import sys
from PyQt6.QtWidgets import QApplication

from package.loginWindow import LoginWindow

def run():
    app = QApplication(sys.argv)
    
    # first part is logging in
    loginWindow = LoginWindow()
    loginWindow.show()

    sys.exit(app.exec())