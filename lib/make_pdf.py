import os
import subprocess

from settings import CMD_PDF_LATEX

def make_pdf(path_template, dir_out, filename, template_value):
    """
    Генерация pdf документа из шаблона.
    :param path_template: путь к шаблону.
    :param dir_out: директория вывода.
    :param filename: имя конечного pdf файла.
    :param template_value: словарь, в котором ключ - это шаблон, а значение - на что его заменить.
    :return:
    """

    # Удаление файлов, с прошлой компиляции.
    for suf in ['aux', 'log', 'pdf', 'tex']:
        remove_path = os.path.join(dir_out, filename + os.path.extsep + suf)
        if os.path.exists(remove_path): os.remove(remove_path)

    # Чтение шаблона.
    file_template = open(path_template, encoding="utf-8")
    document = file_template.read()
    file_template.close()

    # Замена шаблонов на значение.
    for keys in template_value.keys():
        document = document.replace(keys, template_value[keys])

    # Создание tex-овского файла.
    path_out = os.path.join(dir_out, filename + os.path.extsep + 'tex')
    file_out = open(path_out, 'w', encoding="utf-8")
    file_out.write(document)
    file_out.close()

    # Генерация pdf.
    args = [CMD_PDF_LATEX, path_out, f'-output-directory={dir_out}', '-quiet']
    subprocess.call(args)

    return os.path.join(dir_out, filename + os.path.extsep + 'pdf')
