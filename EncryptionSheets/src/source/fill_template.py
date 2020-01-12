import os
import sys
import logging
import argparse
import subprocess

from source.settings import *

parser = argparse.ArgumentParser(description='Генерация шифровок.')
parser.add_argument('-d', '--date', help='дата.', required=True)
parser.add_argument('-s', '--school_subject', help='название предмета.', required=True)
parser.add_argument('-l', '--location', help='населенный пункт.', required=True)
parser.add_argument('-p', '--prefixes', nargs="+", help='префикс шифровки и количество шифровок.', required=True)

args = parser.parse_args(sys.argv[1:])

logging.basicConfig(level=logging.INFO)

prefixes = []
for prefix in args.prefixes:
    data = prefix.split('=')
    if len(data) != 2:
        raise Exception('Неверный префикс шифровки:"%s"' % prefix)

    prefix_value = data[0]
    prefix_count = int(data[1])

    if prefix_count <= 0:
        raise Exception('Неверное количество шифровок:"%s"' % prefix)

    number = 1
    for i in range(prefix_count):
        if number == 13: number += 1
        prefixes.append(prefix_value + '-' + str(number))
        number += 1


def filling_template(template, date, school_subject, location, prefixes):
    """
    Заполнение шаблона
    :param template: шаблон.
    :param date: дата.
    :param school_subject: предмет.
    :param location: место проведения.
    :param prefixes: шифры.
    :return: заполненный шаблон.
    """
    if len(prefixes) % 2 == 1: prefixes.append('Я лишняя!!!')
    logging.info(f'Напечатаны следующие шифровки:{prefixes}')
    template_string = '\TwoEncryption{%s}{%s}{%s}{%%s}{%%s}' % (school_subject, date, location)
    template_document_value = ''
    for i in range(len(prefixes) // 2):
        template_document_value += template_string % (prefixes[2 * i], prefixes[2 * i + 1]) + '\n\t'
    return template.replace('%%{{template_document}}', template_document_value)


for paths in os.listdir(DEFAULT_DIR_OUT):
    os.remove(os.path.join(DEFAULT_DIR_OUT, paths))

logging.debug(f'Путь к файлу с шаблоном: {DEFAULT_PATH_TEMPLATE}')
file_template = open(DEFAULT_PATH_TEMPLATE, encoding="utf-8")
document = filling_template(file_template.read(), args.date, args.school_subject, args.location, prefixes)
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
logging.info(f'Путь к файлу с шаблонами: {path_pdf}')
