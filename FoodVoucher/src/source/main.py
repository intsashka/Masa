import sys
import datetime

from PyQt5 import uic
from PyQt5.QtWidgets import *
from PyQt5.QtWidgets import QFileDialog

from FoodVoucher.src.source.settings_food_voucher import *

import lib.load_excel as load_excel
import FoodVoucher.src.source.logic_food_voucher as logic_food_voucher
from settings import PATH_TO_FOOD_VOUCHER_TEMPLATE, DIR_OUT, PATH_TO_DB_SCHOOL_SUBJECTS


class MainWindow(QMainWindow):
    def __init__(self):
        QMainWindow.__init__(self)
        uic.loadUi(PATH_UI, self)
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

    def clickedButtonCalcVoucher(self):
        """
        Обработка нажатия на клавишу "Рассчитать".
        :return: None.
        """
        count_order_voucher = self.lineEditCountOrderVoucher.text()
        count_spare_voucher = self.lineEditCountSpareVoucher.text()
        try:
            (count_all_voucher, count_calc_space_voucher) = logic_food_voucher.calc_voucher(count_order_voucher,
                                                                                            count_spare_voucher)
            self.lineEditCountCalcAllVoucher.setText(str(count_all_voucher))
            self.lineEditCountCalcSpareVoucher.setText(str(count_calc_space_voucher))
        except Exception as ex:
            QMessageBox.about(self, 'Ошибка', str(ex))
            self.lineEditCountCalcAllVoucher.setText('')
            self.lineEditCountCalcSpareVoucher.setText('')

    def clickedButtonMakeVoucher(self):
        """
        Обработка нажатия на клавишу "Сгенерировать талоны".
        :return: None.
        """
        try:
            self.clickedButtonCalcVoucher()
            path_template = self.lineEditPathTemplate.text()
            dir_out = self.lineEditDirOut.text()
            filename = self.lineEditFilename.text()
            day = self.comboBoxSubjects.currentText()
            count_order_voucher = self.lineEditCountOrderVoucher.text()
            count_spare_voucher = self.lineEditCountSpareVoucher.text()
            path = logic_food_voucher.make_voucher(path_template, dir_out, filename, day, count_order_voucher,
                                                   count_spare_voucher)
            QMessageBox.about(self, 'Талоны сгенерированы!', f'Путь к файлу с талонами:{path}')
        except Exception as ex:
            QMessageBox.about(self, 'Ошибка', str(ex))
            self.lineEditCountCalcAllVoucher.setText('')
            self.lineEditCountCalcSpareVoucher.setText('')

    def setUi(self):
        """
        Формирование UI.
        :return: None.
        """
        self.lineEditPathTemplate.setText(PATH_TO_FOOD_VOUCHER_TEMPLATE)
        self.lineEditDirOut.setText(DIR_OUT)
        self.lineEditFilename.setText(DEFAULT_FILENAME)
        self.loadSubject()

        self.pushButtonPathTemplate.clicked.connect(self.clickedButtonPathTemplate)
        self.pushButtonDirOut.clicked.connect(self.clickedButtonDirOut)
        self.pushButtonCalcVoucher.clicked.connect(self.clickedButtonCalcVoucher)
        self.pushButtonMakeVoucher.clicked.connect(self.clickedButtonMakeVoucher)

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


if __name__ == '__main__':
    app = QApplication(sys.argv)
    mw = MainWindow()
    mw.show()

    sys.exit(app.exec_())
