import math
import os

from FoodVoucher.src.source.settings_food_voucher import VOUCHERS_IN_PAGE

import lib.make_pdf as make_pdf
import lib.load_excel as load_excel
import lib.date_to_rus_string as date_to_rus_string
from settings import PATH_TO_DB_SCHOOL_SUBJECTS


def calc_voucher(count_order_voucher, count_spare_voucher):
    """
    Вычисление общего числа талонов и количество запасных талонов.
    :param count_order_voucher: количество заказанных талонов.
    :param count_spare_voucher: количество запасных талонов.
    :return: (общее число талонов, количество запасных талонов)
    """

    # Проверка, что: количество заказанных талонов - это число > 0.
    try:
        count_order_voucher = int(count_order_voucher)
        if count_order_voucher <= 0: raise Exception()
    except Exception:
        raise Exception('Некорректно задано количество заказанных талонов.')

    # Проверчка, что: количество запасных талонов - это число >= 0.
    try:
        count_spare_voucher = int(count_spare_voucher if len(count_spare_voucher) != 0 else '0')
        if count_spare_voucher < 0: raise Exception()
    except Exception:
        raise Exception('Некорректно задано количество запасных талонов.')

    count_all_voucher = math.ceil((count_order_voucher + count_spare_voucher) / VOUCHERS_IN_PAGE) * VOUCHERS_IN_PAGE
    count_calc_space_voucher = count_all_voucher - count_order_voucher

    return (count_all_voucher, count_calc_space_voucher)


def make_voucher(path_template, dir_out, filename, subject, count_order_voucher, count_spare_voucher):
    # Проверка пути к шаблону.
    if not os.path.isfile(path_template) or os.path.splitext(path_template)[1] != '.tex':
        raise Exception('Некорректно задан путь к шаблону.')

    # Проверка пути к директории вывода.
    if not os.path.isdir(dir_out):
        raise Exception('Некорректно задана директория вывода.')

    # Проверка имени исходного файла.
    if filename.strip() == '':
        raise Exception('Некорректно задано имя файла.')

    # Формирование даты, которая будет печаться на талоне.
    data = load_excel.load_table(filename=PATH_TO_DB_SCHOOL_SUBJECTS)['Данные']
    data = list(filter(lambda item: item['Предмет'] == subject, data))
    if (len(data) != 1):
        raise Exception('Некорректно задан предмет.')
    date = date_to_rus_string.date_to_rus_string(data[0]['Дата']).upper()

    # Вычисление количество всех и запасных талонов.
    (count_all_voucher, count_calc_space_voucher) = calc_voucher(count_order_voucher, count_spare_voucher)
    count_page = count_all_voucher // VOUCHERS_IN_PAGE

    # Заполнение шаблона документа.
    template_value = {}
    template_value[
        '%%{{template_footer}}'] = f'Количество основных талоны: {count_order_voucher}. Количество запасных талонов: {count_calc_space_voucher}.'
    template_value['%%{{template_document}}'] = ('\\VoucherTable{' + date + '}\n') * count_page

    # Генерация pdf.
    return make_pdf.make_pdf(path_template, dir_out, filename, template_value)
