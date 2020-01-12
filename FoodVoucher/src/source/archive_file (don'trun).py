### ЭТО НЕ АКТУАЛЬНЫЙ ФАЙЛ.

import os
import sys
import math
import logging
import datetime
import argparse
import subprocess

from source.settings import *

parser = argparse.ArgumentParser(description='Генерация докумена с талонами.')
parser.add_argument('-c', dest='count_vouchers', type=int, help='требуемое количество талонов.', required=True)
parser.add_argument('-d', dest='add_day', type=int, help='смещение относительно текущего дня.', default=0)

args = parser.parse_args(sys.argv[1:])
count_vouchers = args.count_vouchers
date = datetime.date.today() + datetime.timedelta(args.add_day)

logging.basicConfig(level=logging.INFO)


def date_to_string(date):
    """
    Конвертирование даты в формат отображаемый на талоне.
    :param date: дата.
    :return: строковое представление даты, отображаемое на талоне.
    """
    NAMES_OF_MONTHS = [
        'января',
        'февраля',
        'марта',
        'апреля',
        'мая',
        'июня',
        'июля',
        'августа',
        'сентября',
        'октября',
        'ноября',
        'декабря',
    ]

    string = ''
    string += str(date.day) + ' '
    string += NAMES_OF_MONTHS[date.month - 1].upper() + ' '
    string += str(date.year)
    return string


def filling_template(template, count_vouchers, date):
    """
    Заполнение полей шаблона документа.
    :param template: шаблон.
    :param count_vouchers: неободимое количество талонов.
    :param date: дата.
    :return: заполненый документ.
    """
    count_page = math.ceil(count_vouchers / VOUCHERS_IN_PAGE)
    count_reserve_vouchers = count_page * VOUCHERS_IN_PAGE - count_vouchers

    logging.debug(f'Необходимое количество талонов: {count_vouchers}')
    logging.debug(f'Запасное количество талонов: {count_reserve_vouchers}')
    logging.debug(f'Всего талонов: {count_vouchers + count_reserve_vouchers}')
    logging.debug(f'Дата: {date_to_string(date)}')

    template_document_value = ('\\VoucherTable{' + date_to_string(date) + '}\n') * count_page
    template_footer_value = f'Количество основных талоны: {count_vouchers}. Количество запасных талонов: {count_reserve_vouchers}.'

    template = template.replace('%%{{template_document}}', template_document_value)
    return template.replace('%%{{template_footer}}', template_footer_value)


for paths in os.listdir(DEFAULT_DIR_OUT):
    os.remove(os.path.join(DEFAULT_DIR_OUT, paths))

logging.info(f'Необходимое количество талонов: {count_vouchers}')
logging.info(f'Дата: {date_to_string(date)}')

logging.debug(f'Путь к файлу с шаблоном: {DEFAULT_PATH_TEMPLATE}')
file_template = open(DEFAULT_PATH_TEMPLATE, encoding="utf-8")
document = filling_template(file_template.read(), count_vouchers, date)
file_template.close()

path_out = os.path.join(DEFAULT_DIR_OUT, DEFAULT_FILENAME + '.tex')
logging.debug(f'Путь к выходному файлу: {DEFAULT_PATH_TEMPLATE}')
file_out = open(path_out, 'w', encoding="utf-8")
file_out.write(document)
file_out.close()

args = ["pdflatex", path_out, f'-output-directory={DEFAULT_DIR_OUT}', '-quiet']
subprocess.call(args)

compilation_string = ''
for arg in args: compilation_string = compilation_string + str(arg) + ' '
logging.debug(f'Команда компиляции документа: {compilation_string}')

path_pdf = os.path.join(DEFAULT_DIR_OUT, DEFAULT_FILENAME + '.pdf')
logging.info(f'Путь к файлу с талонами: {path_pdf}')
