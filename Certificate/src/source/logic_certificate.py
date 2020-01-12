import lib.load_excel as load_excel
import lib.make_pdf as make_pdf


def make_certificate(path_template, dir_out, filename, subject_title, path_peoples_input):
    table = load_excel.load_table(path_peoples_input)['Общий список']
    table = list(filter(lambda it: it['ФИО'] != None, table))
    count = 0
    template_document = ''
    for people in table:
        if (people['ФИО'] == None): break
        certificate = "\Certificate{%s}{%s}{%s}{%s}{%s}" % (
            subject_title,
            people['Класс'],
            people['ФИО'],
            people['Учебное заведение'],
            people['Муниципалитет']
        )
        template_document = certificate + '\n' + template_document
        count = count + 1

    return (count, make_pdf.make_pdf(path_template, dir_out, filename, {"%%{{template_document}}": template_document}))
