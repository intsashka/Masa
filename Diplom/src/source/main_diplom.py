import sys
import datetime
import os

from PyQt5 import uic
from PyQt5.QtWidgets import *

from Diplom.src.source.settings_diplom import *

import lib.load_excel as load_excel
import Diplom.src.source.logic_diplom as logic_diplom

from settings import PATH_TO_DB_SCHOOL_SUBJECTS, PATH_TO_DIPLOMA_TEMPLATE, DIR_OUT


class MainWindow(QMainWindow):
    def __init__(self):
        QMainWindow.__init__(self)
        uic.loadUi(PATH_UI, self)

        self.setUi()

    def setUi(self):
        """
        Формирование UI.
        :return: None.
        """
        self.loadSubject()

        self.pushButtonLoad.clicked.connect(self.clickedLoad)
        self.pushButtonLoadPeople.clicked.connect(self.clickedLoadPeople)
        self.pushButtonMake.clicked.connect(self.clickedMake)
        # self.pushButtonMakeCertificate.clicked.connect(self.clickedButtonMakeCertificate)

    def clickedLoad(self):
        names = load_excel.load_sheets_name(self.lineEditProtocol.text())
        self.lineEditSheets.setText(" $ ".join(names))

    def clickedLoadPeople(self):
        peoples = logic_diplom.load_peoples(self.lineEditProtocol.text(), self.lineEditSheets.text())
        self.textBrowserPeoples.setText("\n".join(peoples))

    def clickedMake(self):
        self.pushButtonMake.setEnabled(False)
        (out, path, preview) = logic_diplom.make_diplom(self.lineEditProtocol.text(),
                                                        self.textBrowserPeoples.toPlainText(),
                                                        PATH_TO_DIPLOMA_TEMPLATE,
                                                        DIR_OUT,
                                                        DEFAULT_FILENAME,
                                                        self.lineEditRegNumber.text(),
                                                        self.lineEditNumber.text(),
                                                        self.comboBoxSubject.currentText())

        self.textBrowserOutput.setText(out)
        self.textBrowserPreview.setText(preview)
        QMessageBox.about(self,
                          'Дипломы сгенерированы!',
                          f'Путь к файлу с дипломами: {path}')
        self.pushButtonMake.setEnabled(True)

    def loadSubject(self):
        """
        Загрузка списка дней.
        :return: None.
        """
        data = load_excel.load_table(filename=PATH_TO_DB_SCHOOL_SUBJECTS)['Данные']
        data = sorted(data, key=lambda item: item['Дата'])
        date_min = datetime.datetime.today() - datetime.timedelta(2)
        # data = list(filter(lambda item: item['Дата'] >= date_min, data))
        data = list(map(lambda item: item['Название предмета д.п.'], data))
        newData = []
        for subject in data:
            if (subject not in newData): newData.append(subject)
        self.comboBoxSubject.clear()
        self.comboBoxSubject.addItems(newData)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    mw = MainWindow()
    mw.show()

    sys.exit(app.exec_())
