import sys
from PyQt6.QtWidgets import QWidget, QApplication, QPushButton, QFrame, QMessageBox, QTableWidgetItem, QSizePolicy
from PyQt6.QtCore import pyqtSlot
from PyQt6.QtGui import QIntValidator
from PyQt6.QtSql import QSqlDatabase, QSqlQuery, QSqlQueryModel
from PyQt6.QtWidgets import QGridLayout, QLabel, QLineEdit
from PyQt6 import QtTest

from package.ui.main_ui import Ui_Form

class MainWindow(QWidget):
    def __init__(self):
        super().__init__()

        # Initialize the UI from a separate UI file (created using Qt Designer)
        self.ui = Ui_Form()
        self.ui.setupUi(self)
        
        self.mainDB = QSqlDatabase.addDatabase('QSQLITE', 'main')
        self.mainDB.setDatabaseName('.\\data\\competitiiSportive.sqlite')
        
        if not self.mainDB.open():
            print("Database not opened")
        
        self.partId = self.ui.lineEditIdPart
        self.partId.setValidator(QIntValidator())
        
        # Tab Participanți
        self.numePart = self.ui.lineEditNumePart
        self.prenumePart = self.ui.lineEditPrenumePart
        self.genPart = self.ui.lineEditGenPart
        self.sexPart = self.ui.sexComboBoxPart
        
        self.srcButtonPart = self.ui.searchButtonPart
        self.selButtonPart = self.ui.selectButtonPart
        self.insButtonPart = self.ui.insertButtonPart
        self.updButtonPart = self.ui.updateButtonPart
        self.clrButtonPart = self.ui.clearButtonPart
        self.delButtonPart = self.ui.deleteButtonPart
        
        self.resTablePart = self.ui.tableParticipanti
        self.resTablePart.setSortingEnabled(False)
        self.listButtonsPart = self.ui.frameButtonsPart.findChildren(QPushButton)
        
        self.init_signal_slot_part()
        
        self.showDataPart()
        
        # Tab Tip Competiție
        self.tcompId = self.ui.lineEditIdTComp
        self.tcompId.setValidator(QIntValidator())
        
        self.numeTComp = self.ui.lineEditNumeTComp
        self.grupaTComp = self.ui.lineEditGrupaTComp
        
        self.srcButtonTComp = self.ui.searchButtonTComp
        self.selButtonTComp = self.ui.selectButtonTComp
        self.insButtonTComp = self.ui.insertButtonTComp
        self.updButtonTComp = self.ui.updateButtonTComp
        self.clrButtonTComp = self.ui.clearButtonTComp
        self.delButtonTComp = self.ui.deleteButtonTComp
        
        self.resTableTComp = self.ui.tableTComp
        self.resTableTComp.setSortingEnabled(False)
        self.listButtonsTComp = self.ui.frameButtonsTComp.findChildren(QPushButton)
        
        self.init_signal_slot_tcomp()
        
        self.showDataTComp()
        
        # Tab Statistici
        
        self.tabViewStats = self.ui.tableViewStats
    
        self.comboBoxStats = self.ui.comboBoxStats
        self.lineEditStats = self.ui.lineEditStats
        self.pushButtonStats = self.ui.pushButtonStats
        
        self.pushButtonStats.clicked.connect(self.showStats) 
        
    def showStats(self):
        case = self.comboBoxStats.currentIndex()
        match case:
            case 0:
                if not self.lineEditStats.text():
                    QMessageBox.information(self, "Error", "Inserati o valoare!",
                                    QMessageBox.StandardButton.Ok)
                else:
                    userInput = self.lineEditStats.text().strip()
                    model = QSqlQueryModel()
                    sqlCommand = f"""   SELECT participanti.nume, participanti.prenume 
                                        FROM participanti 
                                        LEFT JOIN participantechipe 
                                        ON participanti.id_part=participantechipe.id_part 
                                        WHERE participantechipe.id_echipa =
                                        (SELECT id_echipa FROM echipe 
                                        WHERE nume='{userInput}');
                                        """
                    model.setQuery(sqlCommand, self.mainDB)
                    
                    if model.lastError().isValid():
                        print(model.lastError().text())
                        QMessageBox.information(self, "Error", "Eroare la query!",
                                        QMessageBox.StandardButton.Ok)
                        
                    else:
                        self.tabViewStats.setModel(model)                   
            case 1:
                if not self.lineEditStats.text():
                    QMessageBox.information(self, "Error", "Inserati o valoare!",
                                    QMessageBox.StandardButton.Ok)
                else:
                    userInput = self.lineEditStats.text().strip()
                    model = QSqlQueryModel()
                    sqlCommand = f"""   SELECT participanti.nume, participanti.prenume 
                                        FROM participanti 
                                        LEFT JOIN participantechipe 
                                        ON participanti.id_part=participantechipe.id_part 
                                        WHERE participantechipe.id_echipa IN
                                        (SELECT id_echipa FROM echipecompetitie
                                        WHERE id_comp=
                                        (SELECT id_comp FROM competitii
                                        WHERE nume='{userInput}'));
                                        """
                    model.setQuery(sqlCommand, self.mainDB)
                    
                    if model.lastError().isValid():
                        print(model.lastError().text())
                        QMessageBox.information(self, "Error", "Eroare la query!",
                                        QMessageBox.StandardButton.Ok)
                        
                    else:
                        self.tabViewStats.setModel(model)
            case 2:
                if not self.lineEditStats.text():
                    QMessageBox.information(self, "Error", "Inserati o valoare!",
                                    QMessageBox.StandardButton.Ok)
                else:
                    userInput = self.lineEditStats.text().strip()
                    model = QSqlQueryModel()
                    sqlCommand = f"""   SELECT echipe.nume 
                                        FROM echipe 
                                        LEFT JOIN echipecompetitie 
                                        ON echipe.id_echipa=echipecompetitie.id_echipa 
                                        WHERE echipecompetitie.id_comp =
                                        (SELECT id_comp FROM competitii 
                                        WHERE nume='{userInput}');
                                        """
                    model.setQuery(sqlCommand, self.mainDB)
                    
                    if model.lastError().isValid():
                        print(model.lastError().text())
                        QMessageBox.information(self, "Error", "Eroare la query!",
                                        QMessageBox.StandardButton.Ok)
                        
                    else:
                        self.tabViewStats.setModel(model)
            case 3:
                if not self.lineEditStats.text():
                    QMessageBox.information(self, "Error", "Inserati o valoare!",
                                    QMessageBox.StandardButton.Ok)
                else:
                    userInput = self.lineEditStats.text().strip()
                    model = QSqlQueryModel()
                    sqlCommand = f"""   SELECT sponsori.nume, sponsoricompetitie.suma_sponsorizare 
                                        FROM sponsori 
                                        LEFT JOIN sponsoricompetitie 
                                        ON sponsori.id_spon=sponsoricompetitie.id_spon 
                                        WHERE sponsoricompetitie.id_comp =
                                        (SELECT id_comp FROM competitii 
                                        WHERE nume='{userInput}');
                                        """
                    model.setQuery(sqlCommand, self.mainDB)
                    
                    if model.lastError().isValid():
                        print(model.lastError().text())
                        QMessageBox.information(self, "Error", "Eroare la query!",
                                        QMessageBox.StandardButton.Ok)
                        
                    else:
                        self.tabViewStats.setModel(model)
            case 4:
                if not self.lineEditStats.text():
                    QMessageBox.information(self, "Error", "Inserati o valoare!",
                                    QMessageBox.StandardButton.Ok)
                else:
                    userInput = self.lineEditStats.text().strip()
                    model = QSqlQueryModel()
                    sqlCommand = f"""   SELECT participanti.nume, participanti.prenume 
                                        FROM participanti 
                                        LEFT JOIN participantechipe 
                                        ON participanti.id_part=participantechipe.id_part 
                                        WHERE participantechipe.id_echipa IN
                                        (SELECT id_echipa FROM echipecompetitie
                                        WHERE id_comp=
                                        (SELECT id_comp FROM competitii
                                        WHERE nume='{userInput}')) AND participantechipe.capitan = 1;
                                        """
                    model.setQuery(sqlCommand, self.mainDB)
                    
                    if model.lastError().isValid():
                        print(model.lastError().text())
                        QMessageBox.information(self, "Error", "Eroare la query!",
                                        QMessageBox.StandardButton.Ok)
                        
                    else:
                        self.tabViewStats.setModel(model)
            case 5:
                if not self.lineEditStats.text():
                    QMessageBox.information(self, "Error", "Inserati o valoare!",
                                    QMessageBox.StandardButton.Ok)
                else:
                    userInput = self.lineEditStats.text().strip()
                    model = QSqlQueryModel()
                    sqlCommand = f"""   SELECT competitii.nume 
                                        FROM competitii
                                        LEFT JOIN sponsoricompetitie 
                                        ON competitii.id_comp=sponsoricompetitie.id_comp 
                                        WHERE sponsoricompetitie.id_spon =
                                        (SELECT id_spon FROM sponsori
                                        WHERE nume='{userInput}');
                                        """
                    model.setQuery(sqlCommand, self.mainDB)
                    
                    if model.lastError().isValid():
                        print(model.lastError().text())
                        QMessageBox.information(self, "Error", "Eroare la query!",
                                        QMessageBox.StandardButton.Ok)
                        
                    else:
                        self.tabViewStats.setModel(model)
            case 6:
                userInput = self.lineEditStats.text().strip()
                model = QSqlQueryModel()
                sqlCommand = f"""   SELECT competitii.nume, SUM(sponsoricompetitie.suma_sponsorizare) AS buget
                                    FROM competitii
                                    LEFT JOIN sponsoricompetitie 
                                    ON competitii.id_comp=sponsoricompetitie.id_comp
                                    WHERE sponsoricompetitie.suma_sponsorizare IN
                                    (SELECT suma_sponsorizare
                                    FROM sponsoricompetitie
                                    WHERE id_comp = competitii.id_comp)
                                    GROUP BY competitii.nume;
                                    """
                model.setQuery(sqlCommand, self.mainDB)
                
                if model.lastError().isValid():
                    print(model.lastError().text())
                    QMessageBox.information(self, "Error", "Eroare la query!",
                                    QMessageBox.StandardButton.Ok)
                    
                else:
                    self.tabViewStats.setModel(model)
            case 7:
                if not self.lineEditStats.text():
                    QMessageBox.information(self, "Error", "Inserati o valoare!",
                                    QMessageBox.StandardButton.Ok)
                else:
                    userInput = self.lineEditStats.text().strip()
                    model = QSqlQueryModel()
                    sqlCommand = f"""   SELECT q1.nume AS 'Nume echipa', q1.nr_part AS 'Număr participanți'
                                    FROM
                                        (
                                            SELECT echipe.nume, COUNT(participantechipe.id_part) AS nr_part
                                            FROM echipe 
                                            LEFT JOIN participantechipe 
                                            ON echipe.id_echipa = participantechipe.id_echipa 
                                            WHERE participantechipe.id_part IN 
                                                (
                                                    SELECT id_part 
                                                    FROM participantechipe 
                                                    WHERE id_echipa = echipe.id_echipa
                                                )  AND echipe.id_echipa IN 
                                                (
                                                    SELECT echipe.id_echipa
                                                    FROM echipe 
                                                    LEFT JOIN echipecompetitie 
                                                    ON echipe.id_echipa=echipecompetitie.id_echipa 
                                                    WHERE echipecompetitie.id_comp =
                                                    (SELECT id_comp FROM competitii 
                                                    WHERE nume='{userInput}')
                                                )
                                            GROUP BY echipe.nume 
                                       ) q1
                                    INNER JOIN (
                                                SELECT MAX(nr_part) AS nmax
                                                FROM
                                                    (
                                                    SELECT echipe.nume, COUNT(participantechipe.id_part) AS nr_part
                                                    FROM echipe 
                                                    LEFT JOIN participantechipe 
                                                    ON echipe.id_echipa = participantechipe.id_echipa 
                                                    WHERE participantechipe.id_part IN 
                                                        (
                                                            SELECT id_part 
                                                            FROM participantechipe 
                                                            WHERE id_echipa = echipe.id_echipa
                                                        ) AND echipe.id_echipa IN 
                                                        (
                                                            SELECT echipe.id_echipa
                                                            FROM echipe 
                                                            LEFT JOIN echipecompetitie 
                                                            ON echipe.id_echipa=echipecompetitie.id_echipa 
                                                            WHERE echipecompetitie.id_comp =
                                                            (SELECT id_comp FROM competitii 
                                                            WHERE nume='{userInput}')
                                                        )
                                                    GROUP BY echipe.nume
                                                    )
                                    ) q2
                                    ON q1.nr_part = q2.nmax;
                                    """
                    model.setQuery(sqlCommand, self.mainDB)
                    
                    if model.lastError().isValid():
                        print(model.lastError().text())
                        QMessageBox.information(self, "Error", "Eroare la query!",
                                        QMessageBox.StandardButton.Ok)
                        
                    else:
                        self.tabViewStats.setModel(model)
            case 8:
                userInput = self.lineEditStats.text().strip()
                model = QSqlQueryModel()
                sqlCommand = f"""   SELECT q1.nume AS 'Nume competiție', q1.nr_echipe AS 'Număr echipe'
                                    FROM
                                        (
                                            SELECT competitii.nume, COUNT(echipecompetitie.id_echipa) AS nr_echipe
                                            FROM competitii 
                                            LEFT JOIN echipecompetitie 
                                            ON competitii.id_comp = echipecompetitie.id_comp 
                                            WHERE echipecompetitie.id_echipa IN 
                                                (
                                                    SELECT id_echipa 
                                                    FROM echipecompetitie 
                                                    WHERE id_comp = competitii.id_comp
                                                ) 
                                            GROUP BY competitii.nume 
                                       ) q1
                                    INNER JOIN (
                                                SELECT MAX(nr_echipe) AS nmax
                                                FROM
                                                    (
                                                    SELECT competitii.nume, COUNT(echipecompetitie.id_echipa) AS nr_echipe
                                                    FROM competitii 
                                                    LEFT JOIN echipecompetitie 
                                                    ON competitii.id_comp = echipecompetitie.id_comp 
                                                    WHERE echipecompetitie.id_echipa IN 
                                                        (
                                                            SELECT id_echipa 
                                                            FROM echipecompetitie 
                                                            WHERE id_comp = competitii.id_comp
                                                        ) 
                                                    GROUP BY competitii.nume 
                                                    )
                                    ) q2
                                    ON q1.nr_echipe = q2.nmax;
                                    """
                model.setQuery(sqlCommand, self.mainDB)
                
                if model.lastError().isValid():
                    print(model.lastError().text())
                    QMessageBox.information(self, "Error", "Eroare la query!",
                                    QMessageBox.StandardButton.Ok)
                    
                else:
                    self.tabViewStats.setModel(model)
            case 9:
                userInput = self.lineEditStats.text().strip()
                model = QSqlQueryModel()
                sqlCommand = f"""   SELECT q1.nume AS 'Nume echipa', q1.nr_comp AS 'Număr competiții'
                                    FROM
                                        (
                                            SELECT echipe.nume, COUNT(echipecompetitie.id_comp) AS nr_comp
                                            FROM echipe 
                                            LEFT JOIN echipecompetitie 
                                            ON echipe.id_echipa = echipecompetitie.id_echipa 
                                            WHERE echipecompetitie.id_comp IN 
                                                (
                                                    SELECT id_comp 
                                                    FROM echipecompetitie 
                                                    WHERE id_echipa = echipe.id_echipa
                                                ) 
                                            GROUP BY echipe.nume 
                                       ) q1
                                    INNER JOIN (
                                                SELECT MAX(nr_comp) AS nmax
                                                FROM
                                                    (
                                                    SELECT echipe.nume, COUNT(echipecompetitie.id_comp) AS nr_comp
                                                    FROM echipe 
                                                    LEFT JOIN echipecompetitie 
                                                    ON echipe.id_echipa = echipecompetitie.id_echipa 
                                                    WHERE echipecompetitie.id_comp IN 
                                                        (
                                                            SELECT id_comp 
                                                            FROM echipecompetitie 
                                                            WHERE id_echipa = echipe.id_echipa
                                                        ) 
                                                    GROUP BY echipe.nume
                                                    )
                                    ) q2
                                    ON q1.nr_comp = q2.nmax;
                                    """
                model.setQuery(sqlCommand, self.mainDB)
                
                if model.lastError().isValid():
                    print(model.lastError().text())
                    QMessageBox.information(self, "Error", "Eroare la query!",
                                    QMessageBox.StandardButton.Ok)
                    
                else:
                    self.tabViewStats.setModel(model)
            case _:
                QMessageBox.information(self, "Error", "Eroare la query! Alegeți o opțiune!",
                                        QMessageBox.StandardButton.Ok)
        pass
    
    def disable_buttonsPart(self):
        # Disable all buttons
        for button in self.listButtonsPart:
            button.setDisabled(True)

    def enable_buttonsPart(self):
        # Enable all buttons
        for button in self.listButtonsPart:
            button.setDisabled(False)
    
    def disable_buttonsTComp(self):
        # Disable all buttons
        for button in self.listButtonsTComp:
            button.setDisabled(True)

    def enable_buttonsTComp(self):
        # Enable all buttons
        for button in self.listButtonsTComp:
            button.setDisabled(False)
        
    def init_signal_slot_part(self):
        self.delButtonPart.clicked.connect(self.delInfoPart)
        self.clrButtonPart.clicked.connect(self.clearInfoPart)
        self.updButtonPart.clicked.connect(self.updInfoPart)
        self.insButtonPart.clicked.connect(self.insInfoPart)
        self.selButtonPart.clicked.connect(self.selInfoPart)
        self.srcButtonPart.clicked.connect(self.srcInfoPart)
    
    def init_signal_slot_tcomp(self):
        self.delButtonTComp.clicked.connect(self.delInfoTComp)
        self.clrButtonTComp.clicked.connect(self.clearInfoTComp)
        self.updButtonTComp.clicked.connect(self.updInfoTComp)
        self.insButtonTComp.clicked.connect(self.insInfoTComp)
        self.selButtonTComp.clicked.connect(self.selInfoTComp)
        self.srcButtonTComp.clicked.connect(self.srcInfoTComp)
    
    def srcInfoPart(self):
         # Function to search for student information and populate the table
        if self.partId.text():
            self.showDataPart(result=self.partId.text().strip())
        else:
            QMessageBox.information(self, "Warning", "Introduceți un ID pentru a efectua căutarea!",
                                    QMessageBox.StandardButton.Ok)

    def srcInfoTComp(self):
         # Function to search for student information and populate the table
        if self.tcompId.text():
            self.showDataTComp(result=self.tcompId.text().strip())
        else:
            QMessageBox.information(self, "Warning", "Introduceți un ID pentru a efectua căutarea!",
                                    QMessageBox.StandardButton.Ok)
    
    def updInfoPart(self):
        self.disable_buttonsPart()
         # Function to update student information
        dataPart = self.getDataPart()

        if self.partId.text() and self.numePart.text():
            
            query = QSqlQuery(self.mainDB)
            sqlCommand = f"""UPDATE participanti SET nume='{self.numePart.text().strip()}', 
                            prenume='{self.prenumePart.text().strip()}', 
                            sex='{self.sexPart.currentText().strip()}', 
                            gen='{self.genPart.text().strip()}' 
                            WHERE id_part={self.partId.text().strip()}"""
            query.prepare(sqlCommand)
            
            if not (query.exec()):
                QMessageBox.information(self, "Eroare", "Eroare la updatare entry. Încercați să introduceți un nou id!",
                                        QMessageBox.StandardButton.Ok)
                self.enable_buttonsPart()
                return
            else:
                QMessageBox.information(self, "OK", "Entry updatat!",
                                        QMessageBox.StandardButton.Ok)
                self.enable_buttonsPart()
                self.clearInfoPart()
                self.showDataPart()
                return
        else:
            QMessageBox.information(self, "Warning", "Introduceți un ID și un nume sau selectați un participant!",
                                    QMessageBox.StandardButton.Ok)
        self.enable_buttonsPart()
    
    def updInfoTComp(self):
        self.disable_buttonsTComp()
         # Function to update student information
        dataTComp = self.getDataTComp()

        if self.tcompId.text() and self.numeTComp.text():
            
            query = QSqlQuery(self.mainDB)
            sqlCommand = f"""UPDATE tipcompetitie SET nume_sport='{self.numeTComp.text().strip()}', 
                            grupa_varsta='{self.grupaTComp.text().strip()}' 
                            WHERE id_tip={self.tcompId.text().strip()}"""
            query.prepare(sqlCommand)
            
            if not (query.exec()):
                QMessageBox.information(self, "Eroare", "Eroare la updatare entry. Încercați să introduceți un nou id!",
                                        QMessageBox.StandardButton.Ok)
                self.enable_buttonsTComp()
                return
            else:
                QMessageBox.information(self, "OK", "Entry updatat!",
                                        QMessageBox.StandardButton.Ok)
                self.enable_buttonsTComp()
                self.clearInfoTComp()
                self.showDataTComp()
                return
        else:
            QMessageBox.information(self, "Warning", "Introduceți un ID și un nume sau selectați un tip de competitie!",
                                    QMessageBox.StandardButton.Ok)
        self.enable_buttonsTComp()

    def insInfoPart(self):
        self.disable_buttonsPart()
        
        dataPart = self.getDataPart()
        
        if self.partId.text() or self.numePart.text():
        
            query = QSqlQuery(self.mainDB)
            sqlCommand = f"""empty"""
            
            if self.partId.text():
                sqlCommand = f"""INSERT INTO participanti (id_part, nume, prenume, sex, gen) VALUES (
                                {self.partId.text().strip()}, 
                                '{self.numePart.text().strip()}', 
                                '{self.prenumePart.text().strip()}', 
                                '{self.sexPart.currentText().strip()}', 
                                '{self.genPart.text().strip()}') 
                                """
            else:
                sqlCommand = f"""INSERT INTO participanti (nume, prenume, sex, gen) VALUES (
                                '{self.numePart.text().strip()}', 
                                '{self.prenumePart.text().strip()}', 
                                '{self.sexPart.currentText().strip()}', 
                                '{self.genPart.text().strip()}') 
                                """
            query.prepare(sqlCommand)
            
            if not (query.exec()):
                # print(sqlCommand)
                # print(query.lastError().text())
                QMessageBox.information(self, "Error", "Eroare la adăugare entry. Încercați să introduceți un nou id!",
                                        QMessageBox.StandardButton.Ok)
                self.enable_buttonsPart()
                
            else:
                QMessageBox.information(self, "OK", "Entry adăugat!",
                                        QMessageBox.StandardButton.Ok)
                self.enable_buttonsPart()
                self.clearInfoPart()
                self.showDataPart()
                

        else:
            QMessageBox.information(self, "Warning", "Introduceți un ID și un nume!",
                                    QMessageBox.StandardButton.Ok)
        
        self.enable_buttonsPart()
        
    def insInfoTComp(self):
        self.disable_buttonsTComp()
        
        dataTComp = self.getDataTComp()
        
        if self.tcompId.text() or self.numeTComp.text():
        
            query = QSqlQuery(self.mainDB)
            sqlCommand = f"""empty"""
            
            if self.partId.text():
                sqlCommand = f"""INSERT INTO tipcompetitie (id_tip, nume_sport, grupa_varsta) VALUES (
                                {self.tcompId.text().strip()}, 
                                '{self.numeTComp.text().strip()}', 
                                '{self.grupaTComp.text().strip()}') 
                                """
            else:
                sqlCommand = f"""INSERT INTO tipcompetitie (nume_sport, grupa_varsta) VALUES (
                                '{self.numeTComp.text().strip()}', 
                                '{self.grupaTComp.text().strip()}') 
                                """
            query.prepare(sqlCommand)
            
            if not (query.exec()):
                # print(sqlCommand)
                # print(query.lastError().text())
                QMessageBox.information(self, "Error", "Eroare la adăugare entry. Încercați să introduceți un nou id!",
                                        QMessageBox.StandardButton.Ok)
                self.enable_buttonsTComp()
                
            else:
                QMessageBox.information(self, "OK", "Entry adăugat!",
                                        QMessageBox.StandardButton.Ok)
                self.enable_buttonsTComp()
                self.clearInfoTComp()
                self.showDataTComp()
                

        else:
            QMessageBox.information(self, "Warning", "Introduceți un ID și un nume!",
                                    QMessageBox.StandardButton.Ok)
        
        self.enable_buttonsTComp()
    
    def getDataPart(self):
        idPart = self.partId.text().strip()
        numePart = self.numePart.text().strip()
        prenumePart = self.prenumePart.text().strip()
        genPart = self.genPart.text().strip()
        sexPart = self.sexPart.currentText().strip()

        dataPart = "(" + idPart +  ", \'" + sexPart +  "\', \'" + genPart + "\', \'" + numePart + "\', \'" + prenumePart + "\')"
        
        return dataPart.strip()

    def getDataTComp(self):
        idTComp = self.tcompId.text().strip()
        numeTComp = self.numeTComp.text().strip()
        grupaTComp = self.grupaTComp.text().strip()

        dataTComp = "(" + idTComp +  ", \'" + numeTComp +  "\', \'" + grupaTComp + "\')"
        
        return dataTComp.strip()
    
    def showDataPart(self, result = None):
        if result == None:
            self.resTablePart.setRowCount(0)
            model = QSqlQueryModel()
            sqlCommand = 'SELECT COUNT(*) FROM participanti'
            model.setQuery(sqlCommand, self.mainDB)
            noRows = model.record(0).value(0)
            self.resTablePart.setRowCount(noRows)
            sqlCommand = 'SELECT id_part, nume, prenume, sex, gen FROM participanti'
            model.setQuery(sqlCommand, self.mainDB)

            if model.lastError().isValid():
                QMessageBox.information(self, "Error", "Eroare la afișare!",
                                    QMessageBox.StandardButton.Ok)
            else:
                # print("aici nu ma bulesc")
                i = 0
                while i < noRows:
                    # print(str(model.record(i).value("id_part")))
                    idPart_item = QTableWidgetItem(str(model.record(i).value("id_part")))
                    self.resTablePart.setItem(i, 0,idPart_item )
                    idPart_item = QTableWidgetItem(str(model.record(i).value("nume")))
                    self.resTablePart.setItem(i, 1,idPart_item )
                    idPart_item = QTableWidgetItem(str(model.record(i).value("prenume")))
                    self.resTablePart.setItem(i, 2,idPart_item )
                    idPart_item = QTableWidgetItem(str(model.record(i).value("sex")))
                    self.resTablePart.setItem(i, 3,idPart_item )
                    idPart_item = QTableWidgetItem(str(model.record(i).value("gen")))
                    self.resTablePart.setItem(i, 4,idPart_item )
                    i = i + 1
            return
        else:
            self.resTablePart.setRowCount(0)
            model = QSqlQueryModel()
            sqlCommand = f"""SELECT id_part, nume, prenume, sex, gen FROM participanti WHERE id_part={result}"""
            model.setQuery(sqlCommand, self.mainDB)
            
            if model.lastError().isValid():
                QMessageBox.information(self, "Error", "Eroare la afișare!",
                                    QMessageBox.StandardButton.Ok)
            else:
                self.resTablePart.setRowCount(1)

                # print("aici nu ma bulesc")
                i = 0
                # while i < noRows:
                    # print(str(model.record(i).value("id_part")))
                idPart_item = QTableWidgetItem(str(model.record(i).value("id_part")))
                self.resTablePart.setItem(i, 0,idPart_item )
                idPart_item = QTableWidgetItem(str(model.record(i).value("nume")))
                self.resTablePart.setItem(i, 1,idPart_item )
                idPart_item = QTableWidgetItem(str(model.record(i).value("prenume")))
                self.resTablePart.setItem(i, 2,idPart_item )
                idPart_item = QTableWidgetItem(str(model.record(i).value("sex")))
                self.resTablePart.setItem(i, 3,idPart_item )
                idPart_item = QTableWidgetItem(str(model.record(i).value("gen")))
                self.resTablePart.setItem(i, 4,idPart_item )
            return
                    # i = i + 1
    
    def showDataTComp(self, result = None):
        if result == None:
            self.resTableTComp.setRowCount(0)
            model = QSqlQueryModel()
            sqlCommand = 'SELECT COUNT(*) FROM tipcompetitie'
            model.setQuery(sqlCommand, self.mainDB)
            noRows = model.record(0).value(0)
            self.resTableTComp.setRowCount(noRows)
            sqlCommand = 'SELECT id_tip, nume_sport, grupa_varsta FROM tipcompetitie'
            model.setQuery(sqlCommand, self.mainDB)

            if model.lastError().isValid():
                QMessageBox.information(self, "Error", "Eroare la afișare!",
                                    QMessageBox.StandardButton.Ok)
            else:
                # print("aici nu ma bulesc")
                i = 0
                while i < noRows:
                    # print(str(model.record(i).value("id_part")))
                    idTComp_item = QTableWidgetItem(str(model.record(i).value("id_tip")))
                    self.resTableTComp.setItem(i, 0,idTComp_item )
                    idTComp_item = QTableWidgetItem(str(model.record(i).value("nume_sport")))
                    self.resTableTComp.setItem(i, 1,idTComp_item )
                    idTComp_item = QTableWidgetItem(str(model.record(i).value("grupa_varsta")))
                    self.resTableTComp.setItem(i, 2,idTComp_item )
                    i = i + 1
            return
        else:
            self.resTableTComp.setRowCount(0)
            model = QSqlQueryModel()
            sqlCommand = f"""SELECT id_tip, nume_sport, grupa_varsta FROM tipcompetitie WHERE id_tip={result}"""
            model.setQuery(sqlCommand, self.mainDB)
            
            if model.lastError().isValid():
                QMessageBox.information(self, "Error", "Eroare la afișare!",
                                    QMessageBox.StandardButton.Ok)
            else:
                self.resTableTComp.setRowCount(1)

                # print("aici nu ma bulesc")
                i = 0
                # while i < noRows:
                    # print(str(model.record(i).value("id_part")))
                idTComp_item = QTableWidgetItem(str(model.record(i).value("id_tip")))
                self.resTableTComp.setItem(i, 0,idTComp_item )
                idTComp_item = QTableWidgetItem(str(model.record(i).value("nume_sport")))
                self.resTableTComp.setItem(i, 1,idTComp_item )
                idTComp_item = QTableWidgetItem(str(model.record(i).value("grupa_varsta")))
                self.resTableTComp.setItem(i, 2,idTComp_item )
            return
                    # i = i + 1
    
    def clearInfoPart(self):
        self.partId.clear()
        self.numePart.clear()
        self.prenumePart.clear()
        self.genPart.clear()
        self.sexPart.setCurrentIndex(0)
        self.showDataPart()
        self.partId.setEnabled(True)
        
    def clearInfoTComp(self):
        self.tcompId.clear()
        self.numeTComp.clear()
        self.grupaTComp.clear()
        self.showDataTComp()
        self.tcompId.setEnabled(True)
    
    def selInfoPart(self):
        selRow = self.resTablePart.currentRow()
        if selRow != -1:
            self.partId.setEnabled(False)
            id = self.resTablePart.item(selRow, 0).text().strip()
            nume = self.resTablePart.item(selRow, 1).text().strip()
            prenume = self.resTablePart.item(selRow, 2).text().strip()
            sex = self.resTablePart.item(selRow, 4).text().strip()
            gen = self.resTablePart.item(selRow, 3).text().strip()

            self.partId.setText(id)
            self.numePart.setText(nume)
            self.prenumePart.setText(prenume)
            self.sexPart.setCurrentText(sex)
            self.genPart.setText(gen)
        else:
            QMessageBox.information(self, "Warning", "Selectează un entry!",
                                    QMessageBox.StandardButton.Ok)
    
    def selInfoTComp(self):
        selRow = self.resTableTComp.currentRow()
        if selRow != -1:
            self.tcompId.setEnabled(False)
            id = self.resTableTComp.item(selRow, 0).text().strip()
            nume = self.resTableTComp.item(selRow, 1).text().strip()
            grupa = self.resTableTComp.item(selRow, 2).text().strip()

            self.tcompId.setText(id)
            self.numeTComp.setText(nume)
            self.grupaTComp.setText(grupa)
        else:
            QMessageBox.information(self, "Warning", "Selectează un entry!",
                                    QMessageBox.StandardButton.Ok)
    
    def delInfoPart(self):
        selRow = self.resTablePart.currentRow()
        if selRow != -1:
            selected_option = QMessageBox.warning(self, "Warning", "Sigur stergeti entry-ul?",
                                                  QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.Cancel)

            if selected_option == QMessageBox.StandardButton.Yes:
                idPart = self.resTablePart.item(selRow, 0).text().strip()
                model = QSqlQueryModel()
                sqlCommand = f"""DELETE FROM participantechipe WHERE id_part={idPart};
                                 """
                model.setQuery(sqlCommand, self.mainDB)
                
                if model.lastError().isValid():
                    print(model.lastError().text())
                    QMessageBox.information(self, "Error", "Eroare la ștergere!",
                                    QMessageBox.StandardButton.Ok)
                    
                else:
                    sqlCommand = f"""DELETE FROM participanti WHERE id_part={idPart};
                                 """
                    model.setQuery(sqlCommand, self.mainDB)
                    
                    if model.lastError().isValid():
                        print(model.lastError().text())
                        QMessageBox.information(self, "Error", "Eroare la ștergere!",
                                    QMessageBox.StandardButton.Ok)
                    
                    else:
                        self.clearInfoPart()
                        self.showDataPart()
                        QMessageBox.information(self, "OK", "Entry șters!",
                                        QMessageBox.StandardButton.Ok)


        else:
            if not self.partId.text():
                QMessageBox.information(self, "Warning", "Alegeti un participant pentru stergere!",
                                    QMessageBox.StandardButton.Ok)
            else:
                selected_option = QMessageBox.warning(self, "Warning", "Sigur stergeti entry-ul?",
                                                  QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.Cancel)

            if selected_option == QMessageBox.StandardButton.Yes:
                idPart = self.partId.text().strip()
                model = QSqlQueryModel()
                sqlCommand = f"""DELETE FROM participantechipe WHERE id_part={idPart};
                                 """
                model.setQuery(sqlCommand, self.mainDB)
                
                if model.lastError().isValid():
                    print(model.lastError().text())
                    QMessageBox.information(self, "Error", "Eroare la ștergere!",
                                    QMessageBox.StandardButton.Ok)
                    
                else:
                    sqlCommand = f"""DELETE FROM participanti WHERE id_part={idPart};
                                 """
                    model.setQuery(sqlCommand, self.mainDB)
                    
                    if model.lastError().isValid():
                        print(model.lastError().text())
                        QMessageBox.information(self, "Error", "Eroare la ștergere!",
                                    QMessageBox.StandardButton.Ok)
                    
                    else:
                        self.clearInfoPart()
                        self.showDataPart()
                        QMessageBox.information(self, "OK", "Entry șters!",
                                        QMessageBox.StandardButton.Ok)
    
    def delInfoTComp(self):
        selRow = self.resTableTComp.currentRow()
        if selRow != -1:
            selected_option = QMessageBox.warning(self, "Warning", "Sigur stergeti entry-ul? Se vor șterge și toate competițiile de acest tip!",
                                                  QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.Cancel)

            if selected_option == QMessageBox.StandardButton.Yes:
                idTComp = self.resTableTComp.item(selRow, 0).text().strip()
                model = QSqlQueryModel()
                sqlCommand = f"""DELETE FROM echipecompetitie WHERE id_comp IN (SELECT id_comp FROM competitii WHERE id_tip={idTComp});
                                 """
                model.setQuery(sqlCommand, self.mainDB)
                
                if model.lastError().isValid():
                    QMessageBox.information(self, "Error", "Eroare la ștergere!",
                                    QMessageBox.StandardButton.Ok)
                    
                else:
                    
                    sqlCommand = f"""DELETE FROM sponsoricompetitie WHERE id_comp IN (SELECT id_comp FROM competitii WHERE id_tip={idTComp});
                                    """
                    model.setQuery(sqlCommand, self.mainDB)
                    
                    if model.lastError().isValid():
                        QMessageBox.information(self, "Error", "Eroare la ștergere!",
                                        QMessageBox.StandardButton.Ok)
                    else:
                        sqlCommand = f"""DELETE FROM competitii WHERE id_tip={idTComp};
                                         """
                        model.setQuery(sqlCommand, self.mainDB)
                    
                        if model.lastError().isValid():
                            QMessageBox.information(self, "Error", "Eroare la ștergere!",
                                            QMessageBox.StandardButton.Ok)
                        else:
                            sqlCommand = f"""DELETE FROM tipcompetitie WHERE id_tip={idTComp};
                                        """
                            model.setQuery(sqlCommand, self.mainDB)
                        
                            if model.lastError().isValid():
                                QMessageBox.information(self, "Error", "Eroare la ștergere!",
                                                QMessageBox.StandardButton.Ok)
                            else:
                                self.clearInfoTComp()
                                self.showDataTComp()
                                QMessageBox.information(self, "OK", "Entry șters!",
                                                QMessageBox.StandardButton.Ok)


        else:
            if not self.tcompId.text():
                QMessageBox.information(self, "Warning", "Alegeti un tip de competitie pentru stergere!",
                                    QMessageBox.StandardButton.Ok)
            else:
                selected_option = QMessageBox.warning(self, "Warning", "Sigur stergeti entry-ul? Se vor șterge și toate competițiile de acest tip!",
                                                  QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.Cancel)

            if selected_option == QMessageBox.StandardButton.Yes:
                idTComp = self.tcompId.text().strip()
                model = QSqlQueryModel()
                sqlCommand = f"""DELETE FROM echipecompetitie WHERE id_comp IN (SELECT id_comp FROM competitii WHERE id_tip={idTComp});
                                 """
                model.setQuery(sqlCommand, self.mainDB)
                
                if model.lastError().isValid():
                    QMessageBox.information(self, "Error", "Eroare la ștergere!",
                                    QMessageBox.StandardButton.Ok)
                    
                else:
                    
                    sqlCommand = f"""DELETE FROM sponsoricompetitie WHERE id_comp IN (SELECT id_comp FROM competitii WHERE id_tip={idTComp});
                                    """
                    model.setQuery(sqlCommand, self.mainDB)
                    
                    if model.lastError().isValid():
                        QMessageBox.information(self, "Error", "Eroare la ștergere!",
                                        QMessageBox.StandardButton.Ok)
                    else:
                        sqlCommand = f"""DELETE FROM competitii WHERE id_tip={idTComp};
                                         """
                        model.setQuery(sqlCommand, self.mainDB)
                    
                        if model.lastError().isValid():
                            QMessageBox.information(self, "Error", "Eroare la ștergere!",
                                            QMessageBox.StandardButton.Ok)
                        else:
                            sqlCommand = f"""DELETE FROM tipcompetitie WHERE id_tip={idTComp};
                                        """
                            model.setQuery(sqlCommand, self.mainDB)
                        
                            if model.lastError().isValid():
                                QMessageBox.information(self, "Error", "Eroare la ștergere!",
                                                QMessageBox.StandardButton.Ok)
                            else:
                                self.clearInfoTComp()
                                self.showDataTComp()
                                QMessageBox.information(self, "OK", "Entry șters!",
                                                QMessageBox.StandardButton.Ok)
