import os

from settings import ROOT_DIR

# Имя выходного файла (по умолчанию).
DEFAULT_FILENAME = 'Талоны'

# Путь к файлу с дизайном интерфейса.
PATH_UI = os.path.join(ROOT_DIR, 'FoodVoucher/src/ui/main_window.ui')

# Количество талонов на одном листе.
VOUCHERS_IN_PAGE = 18
