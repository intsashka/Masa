import datetime
import subprocess
import argparse
import sys
from openpyxl import load_workbook

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
    string += NAMES_OF_MONTHS[date.month - 1].lower() + ' '
    string += str(date.year)
    return string

PATH = r'C:\intsashka\work\ВсОШ 2019\Программы\Masa\EncryptionSheets\data\data.xlsx'

parser = argparse.ArgumentParser(description='Генерация шифровок.')
parser.add_argument('-p', '--prefixes', nargs="+", help='префикс шифровки и количество шифровок.', required=True)
args = parser.parse_args(sys.argv[1:])

wb = load_workbook(filename=PATH, read_only=True)
ws = wb['Данные']

STR_TITLE = 'Название'
STR_SCHOOL_SUBJECT = 'Название предмета'
STR_DATA = 'Дата'
STR_LOCATION = 'Место проведения'

print(datetime.today())

rows = tuple(ws.rows)
head = rows[0]
table = rows[1:]
data = []
for row in table:
    data_row = {}
    for i in range(len(head)):
        data_row[head[i].value] = row[i].value
    data.append(data_row)

print('Список возможных предметов:')
for i in range(len(data)):
    subject = data[i]
    print(f'\t{i}:{subject[STR_TITLE]}')
print()

number = int(input('Введите номер предмета:'))
if (number not in range(len(data))):
    raise Exception('Некорректный номер предмета')


subject = data[number]
print('Выбранный предмет:')
for key in subject.keys():
    if key == STR_DATA:
        print(f'\t{key} = {date_to_string(subject[key])}')
    else:
        print(f'\t{key} = {subject[key]}')
print()

sub_args = [
    'python',
    'fill_template.py',
    '--date', date_to_string(subject[STR_DATA]),
    '--school_subject', subject[STR_SCHOOL_SUBJECT],
    '--location', subject[STR_LOCATION],
    '--prefixes', *args.prefixes
]

subprocess.call(sub_args)
