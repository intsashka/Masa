import os
import lib.load_excel as load_excel
import lib.date_to_rus_string as date_to_ru_string
import lib.make_pdf as make_pdf
from settings import PATH_TO_DB_SCHOOL_SUBJECTS


def make_encryption_sheets(path_template, dir_out, filename, subject_title, count_players):
    """
    Генерация шифровок.
    :param path_template: путь к файлу с шаблоном.
    :param dir_out: путь к директории вывода.
    :param filename: имя итоговой файла.
    :param subject_title: предмет.
    :param count_players: количество участников по классам.
    :return:
    """

    # Проверка пути к шаблону.
    if not os.path.isfile(path_template) or os.path.splitext(path_template)[1] != '.tex':
        raise Exception('Некорректно задан путь к шаблону.')

    # Проверка пути к директории вывода.
    if not os.path.isdir(dir_out):
        raise Exception('Некорректно задана директория вывода.')

    # Проверка имени итогового файла.
    if filename.strip() == '':
        raise Exception('Некорректно задано имя файла.')

    # Проверка корректности заданого предмета.
    data = load_excel.load_table(filename=PATH_TO_DB_SCHOOL_SUBJECTS)['Данные']
    data = list(filter(lambda item: item['Предмет'] == subject_title, data))
    if (len(data) != 1):
        raise Exception('Некорректно задан предмет.')
    else:
        subject = data[0]

    # Проверка, что количество учеников задано корректно.
    try:
        for key in count_players.keys():
            count_players[key] = int(count_players[key])
            if count_players[key] < 0:
                raise Exception()
    except Exception:
        raise Exception('Некорректно задано количество учеников.')

    codes = []

    p = {}
    for key in sorted(count_players.keys()):
        count = count_players[key]
        if count == 0: continue
        numbers = list(range(1, count + 1))
        if count >= 13:
            numbers.append(count + 1)
            numbers.remove(13)
            numbers.sort()

        prefix = subject[f'Шифр {key} класс']
        if (prefix == None) or (len(prefix) == 0):
            raise Exception('Заданы не существующие шифровки.')
        else:
            p[prefix] = p.get(prefix, 0) + count

    for prefix in p.keys():
        count = p[prefix]
        if count == 0: continue
        numbers = list(range(1, count + 1))
        if count >= 13:
            numbers.append(count + 1)
            numbers.remove(13)
            numbers.sort()
        codes.extend(list(map(lambda number: prefix + '-' + ("%02d" % number), numbers)))

    if (len(codes) % 2 == 1): codes.append('Я лишняя!!!')

    title = subject['Название предмета д.п.']
    title = title[:1].lower() + title[1:]
    '\TwoEncryption{истории}{18 января 2019}{г. Красноярск}{РЯ11-19}{РЯ11-20}'
    temp = '\TwoEncryption{%s}{%s}{%s}{%%s}{%%s}\n' % (
        title,
        date_to_ru_string.date_to_rus_string(subject['Дата']),
        subject['Место проведения'])

    template_value = ''
    for i in range(0, len(codes) - 1, 2):
        template_value = template_value + (temp % (codes[i], codes[i + 1]))

    return make_pdf.make_pdf(path_template, dir_out, filename, {'%%{{template_document}}':template_value})