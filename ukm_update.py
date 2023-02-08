import os
import time
import re
import datetime
import shutil
import psutil
import win32api
import win32net
import logging
import openpyxl

logging.basicConfig(level=logging.INFO, filename="log.txt", filemode="w")

# подключение листа Excel
wb = openpyxl.load_workbook(f'addresses.xlsx')
sheet = wb.active


for i in range(1, sheet.max_row + 1):
    try:
        computer = sheet[f'A{i}'].value
        dst_path = rf'\\{computer}\c$\Program Files\lillo-win\ukmupman'
        login = '.\администратор'
        password = 'qwerty-bc'
        mount_command = rf'net use /user:{login} "{dst_path}" {password}'
        mount_result = os.system(mount_command)
        src_path = rf'C:\Users\Dorofeev.E.BOOKCENTRE\Desktop\ssPyQt5_report_creation'
        tree_name = '\\update'
        if os.path.exists(dst_path + tree_name):
            shutil.rmtree(dst_path + tree_name)
        print(shutil.copytree(src_path + tree_name, dst_path + tree_name))

        if os.path.isdir(dst_path + tree_name):
            logging.info(f"{computer}")
        else:
            logging.error(f'{computer}')
    except Exception as exc:
        print(exc)
        logging.error(f'{computer}')
