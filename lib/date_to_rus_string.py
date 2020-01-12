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

def date_to_rus_string(date):
    """
    Конвертирование даты в формат: 24 декабря 2018
    :param date: дата.
    :return: строковое представление даты.
    """
    string = ''
    string += str(date.day) + ' '
    string += NAMES_OF_MONTHS[date.month - 1] + ' '
    string += str(date.year) + ' года'
    return string


def month_to_rus_string(date):
    return NAMES_OF_MONTHS[date.month - 1]
