import shutil
import openpyxl
import os

# source_path = r'\\itech51\share51'
# source_path = r'\\operator4\c$\zDistr'
# dest_path = r'C:\Users\Dorofeev.E.BOOKCENTRE\Desktop\ssPyQt5_report_creation'
# file_name = '\\sas.txt'

# shutil.copyfile(source_path + file_name, dest_path + file_name)
# print(source_path + file_name, dest_path + file_name)

# создание файла excel
filepath = r"C:\Users\Dorofeev.E.BOOKCENTRE\Desktop\ssPyQt5_report_creation\boba.xlsx"
wb = openpyxl.Workbook()
wb.save(filepath)

# удаление файла
if os.path.exists(r'C:\Users\Dorofeev.E.BOOKCENTRE\Desktop\ssPyQt5_report_creation\boba.xlsx'):
    os.remove(
        r'C:\Users\Dorofeev.E.BOOKCENTRE\Desktop\ssPyQt5_report_creation\boba.xlsx')
