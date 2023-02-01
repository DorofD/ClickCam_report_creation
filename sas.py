import shutil
import openpyxl
import os

# # source_path = r'\\itech51\share51'
# source_path = r'\\operator4\c$\zDistr'
# dest_path = r'C:\Users\Dorofeev.E.BOOKCENTRE\Desktop\ssPyQt5_report_creation'
# file_name = '\\sas.txt'

# shutil.copyfile(source_path + file_name, dest_path + file_name)
# print(source_path + file_name, dest_path + file_name)

# создание файла excel
# boba = 'boba'
# filepath = rf"C:\Users\Dorofeev.E.BOOKCENTRE\Desktop\ssPyQt5_report_creation\{boba}.xlsx"
# wb = openpyxl.Workbook()
# wb.save(filepath)

# # # удаление файла
# if os.path.exists(r'C:\Users\Dorofeev.E.BOOKCENTRE\Desktop\ssPyQt5_report_creation\boba.xlsx'):
#     os.remove(
#         r'C:\Users\Dorofeev.E.BOOKCENTRE\Desktop\ssPyQt5_report_creation\boba.xlsx')


wb = openpyxl.load_workbook(f'addresses.xlsx')
sheet = wb.active
print(sheet.max_row)

for i in range(1, sheet.max_row + 1):
    print(sheet[f'A{i}'].value)
    # print(i)
