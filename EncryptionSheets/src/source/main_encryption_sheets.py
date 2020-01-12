import sys
import datetime

from PyQt5 import uic
from PyQt5.QtWidgets import *
from PyQt5.QtWidgets import QFileDialog

from EncryptionSheets.src.source.settings_encryption_sheets import *

import lib.load_excel as load_excel
import lib.date_to_rus_string as date_to_rus_string
import EncryptionSheets.src.source.logic_encryption_sheets as logic_encryption_sheets
from settings import DIR_OUT, PATH_TO_ENCRYPTION_SHEETS_TEMPLATE, PATH_TO_DB_SCHOOL_SUBJECTS


class MainWindow(QMainWindow):
    def __init__(self):
        QMainWindow.__init__(self)
        uic.loadUi(PATH_UI, self)
        self.lineEditCountPlayers = [
            self.lineEditCountPlayer7,
            self.lineEditCountPlayer8,
            self.lineEditCountPlayer9,
            self.lineEditCountPlayer10,
            self.lineEditCountPlayer11
        ]

        self.lineEditPrefixes = [
            self.lineEditPrefix7,
            self.lineEditPrefix8,
            self.lineEditPrefix9,
            self.lineEditPrefix10,
            self.lineEditPrefix11
        ]

        self.numberClass = [7, 8, 9, 10, 11]

        self.setUi()

    def clickedButtonPathTemplate(self):
        """
        Обработка нажатия на клавишу "Задать файл шаблона".
        :return: None.
        """
        filename = QFileDialog.getOpenFileName(self, 'Выбор файла шаблона', 'C:\\', "Tex files (*.tex)")[0]
        if filename != '': self.lineEditPathTemplate.setText(filename)

    def clickedButtonDirOut(self):
        """
        Обработка нажатия на клавишу "Задать директорию вывода".
        :return: None.
        """
        dialog = QFileDialog()
        dialog.setFileMode(QFileDialog.Directory)
        dialog.setAcceptMode(QFileDialog.AcceptOpen)
        if dialog.exec_():
            filename = dialog.selectedFiles()[0]
            self.lineEditDirOut.setText(filename)

    def clickedButtonMakeEncryptionSheets(self):
        """
        Обработка нажатия на клавишу "Сгенерировать".
        :return: None.
        """
        path_template = self.lineEditPathTemplate.text()
        dir_out = self.lineEditDirOut.text()
        filename = self.lineEditFilename.text()
        subject = self.comboBoxSubjects.currentText()
        count_players = {}
        for i in range(len(self.numberClass)):
            text = self.lineEditCountPlayers[i].text().strip()
            if len(text) != 0:
                count_players[self.numberClass[i]] = text

        path = logic_encryption_sheets.make_encryption_sheets(path_template, dir_out, filename, subject, count_players)
        QMessageBox.about(self, 'Шифровки сгенерированы!', f'Путь к файлу с шифровками: {path}')

    def setUi(self):
        """
        Формирование UI.
        :return: None.
        """
        self.comboBoxSubjects.currentIndexChanged.connect(self.selectSubject)

        self.lineEditPathTemplate.setText(PATH_TO_ENCRYPTION_SHEETS_TEMPLATE)
        self.lineEditDirOut.setText(DIR_OUT)
        self.lineEditFilename.setText(DEFAULT_FILENAME)
        self.loadSubject()

        self.pushButtonPathTemplate.clicked.connect(self.clickedButtonPathTemplate)
        self.pushButtonDirOut.clicked.connect(self.clickedButtonDirOut)
        self.pushButtonMakeEncryptionSheets.clicked.connect(self.clickedButtonMakeEncryptionSheets)

    def loadSubject(self):
        """
        Загрузка списка дней.
        :return: None.
        """
        data = load_excel.load_table(filename=PATH_TO_DB_SCHOOL_SUBJECTS)['Данные']
        data = sorted(data, key=lambda item: item['Дата'])
        date_min = datetime.datetime.today() - datetime.timedelta(2)
        data = list(filter(lambda item: item['Дата'] >= date_min, data))
        self.comboBoxSubjects.clear()
        self.comboBoxSubjects.addItems(list(map(lambda item: item['Предмет'], data)))


    def selectSubject(self):
        """
        Обработка выбора предмета из списка.
        :return: None.
        """
        select_subject = self.comboBoxSubjects.currentText()
        data = load_excel.load_table(filename=PATH_TO_DB_SCHOOL_SUBJECTS)['Данные']
        subject = list(filter(lambda item: item['Предмет'] == select_subject, data))[0]

        self.lineEditTitleSubject.setText(subject['Название предмета д.п.'].lower())
        self.lineEditDate.setText(date_to_rus_string.date_to_rus_string(subject['Дата']))
        self.lineEditLocation.setText(subject['Место проведения'])

        for i in range(len(self.lineEditCountPlayers)):
            if (subject[f'Шифр {self.numberClass[i]} класс'] != None):
                self.lineEditCountPlayers[i].setEnabled(True)
                self.lineEditPrefixes[i].setText(subject[f'Шифр {self.numberClass[i]} класс'])
            else:
                self.lineEditCountPlayers[i].setEnabled(False)
                self.lineEditCountPlayers[i].setText('')
                self.lineEditPrefixes[i].setText('')

if __name__ == '__main__':
    app = QApplication(sys.argv)
    mw = MainWindow()
    mw.show()

    sys.exit(app.exec_())
