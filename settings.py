import os

ROOT_DIR = os.path.dirname(os.path.abspath(__file__))

# Путь к базе предметов.
PATH_TO_DB_SCHOOL_SUBJECTS = 'C:\intsashka\work\ВсОШ 2020\Базы данных\База предметов ВСОШ 2020.xlsx'

# Директория вывода.
DIR_OUT = 'C:\intsashka\work\ВсОШ 2020\Результаты генерации'

# Пути к шаблонам
PATH_TO_DIPLOMA_TEMPLATE = 'C:\intsashka\work\ВсОШ 2020\Шаблоны документов\Шаблон диплома.tex'
PATH_TO_CERTIFICATE_TEMPLATE = 'C:\intsashka\work\ВсОШ 2020\Шаблоны документов\Шаблон сертификата.tex'
PATH_TO_ENCRYPTION_SHEETS_TEMPLATE = 'C:\intsashka\work\ВсОШ 2020\Шаблоны документов\Шаблон шифровки.tex'
PATH_TO_FOOD_VOUCHER_TEMPLATE = 'C:\intsashka\work\ВсОШ 2020\Шаблоны документов\Шалон талона.tex'

# Команда для генерации
CMD_PDF_LATEX = 'pdflatex'