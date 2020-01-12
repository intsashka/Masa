import sys
import datetime

from PyQt5 import uic
from PyQt5.QtWidgets import *

from Certificate.src.source.settings_certificate import *

import lib.load_excel as load_excel
import Certificate.src.source.logic_certificate as logic_certificate
from settings import PATH_TO_CERTIFICATE_TEMPLATE, DIR_OUT, PATH_TO_DB_SCHOOL_SUBJECTS


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
        self.lineEditPathTemplate.setText(PATH_TO_CERTIFICATE_TEMPLATE)
        self.lineEditDirOut.setText(DIR_OUT)
        self.lineEditFilename.setText(DEFAULT_FILENAME)
        self.loadSubject()

        self.pushButtonMakeCertificate.clicked.connect(self.clickedButtonMakeCertificate)

    def clickedButtonMakeCertificate(self):
        """
        Событие: нажатие на кнопку "Сгенерировать".
        :return:
        """
        subject_title = self.comboBoxSubjects.currentText()
        data = load_excel.load_table(filename=PATH_TO_DB_SCHOOL_SUBJECTS)['Данные']
        data = list(filter(lambda it: it['Название предмета д.п.'].lower() == subject_title, data))
        subject_title = data[0]['Название предмета д.п.']
        subject_title = subject_title[0:1].lower() + subject_title[1:]
        self.pushButtonMakeCertificate.setEnabled(False)
        (count, path) = logic_certificate.make_certificate(path_template=self.lineEditPathTemplate.text(),
                                                           dir_out=self.lineEditDirOut.text(),
                                                           filename=self.lineEditFilename.text(),
                                                           subject_title=subject_title,
                                                           path_peoples_input=os.path.abspath(
                                                               self.lineEditPathPeoplesInput.text()))

        QMessageBox.about(self,
                          'Сертификаты сгенерированы!',
                          f'Количество: {count}.\nПуть к файлу с сертификатами: {path}')
        self.pushButtonMakeCertificate.setEnabled(True)

    def loadSubject(self):
        """
        Загрузка списка дней.
        :return: None.
        """
        data = load_excel.load_table(filename=PATH_TO_DB_SCHOOL_SUBJECTS)['Данные']
        data = sorted(data, key=lambda item: item['Дата'])
        date_min = datetime.datetime.today() - datetime.timedelta(2)
        data = list(filter(lambda item: item['Дата'] >= date_min, data))
        data = list(map(lambda item: item['Название предмета д.п.'], data))
        newData = []
        for subject in data:
            if (subject not in newData): newData.append(subject)
        newData = list(map(lambda item: item.lower(), newData))
        self.comboBoxSubjects.clear()
        self.comboBoxSubjects.addItems(newData)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    mw = MainWindow()
    mw.show()

    sys.exit(app.exec_())
