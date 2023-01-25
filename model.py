import sqlite3 as sq
import openpyxl
import os
import shutil
from ftplib import FTP
import re
import datetime


def db_update(file):
    try:
        conn = sq.connect('database.db')
        cursor = conn.cursor()
        wb = openpyxl.load_workbook(file)  # подключение листа Excel
        sheet = wb.active
        # перед действием ниже нужно дописать проверки импортированного файла
        query = """
            SELECT * FROM contracts
        """
        cursor.execute(query)
        query = """
            DELETE FROM contracts
        """
        cursor.execute(query)
        # range(len(sheet["A"]) - 1)
        i = 1
        for row in range(len(sheet["A"]) - 2):
            if sheet['A'][i].value:
                query = f""" 
                    INSERT INTO contracts (pid, shop_name, wan_type, ip, legal_entity, isp, contract, shop_address, sd_phone, sd_email) 
                    VALUES ('{sheet['A'][i].value}',
                    '{sheet['B'][i].value}',
                    '{sheet['C'][i].value}',
                    '{sheet['D'][i].value}',
                    '{sheet['E'][i].value}',
                    '{sheet['F'][i].value}',
                    '{sheet['G'][i].value}',
                    '{sheet['H'][i].value}',
                    '{sheet['I'][i].value}',
                    '{sheet['J'][i].value}'
                    )
                """
                cursor.execute(query)
                i += 1
        conn.commit()
        conn.close()
        return True
    except Exception as exc:
        conn.close()
        print(exc)
        return False


def get_contract_id(id):
    conn = sq.connect('database.db')
    cursor = conn.cursor()
    query = f"""SELECT * FROM contracts
        WHERE id = '{id}'"""
    cursor.execute(query)
    result = cursor.fetchall()
    conn.close()
    return result


def get_one_report(operator):
    db_path = 1
    pass


def get_all_reports(operator):
    pass


def get_report(operator):
    operators = {
        0: ['operator11', 'operator2', 'operator33', 'operator4', 'operator5'],
        1: 'operator11',
        2: 'operator2',
        3: 'operator33',
        4: 'operator4',
        5: 'operator5',
    }
    if operator == 0:
        file_path = get_all_reports(operators[operator])
    else:
        file_path = get_one_report(operators[operator])
    print(operators[operator])
    try:
        source_path = r'\\operator4\c$\zDistr'
        dest_path = r'C:\Users\Dorofeev.E.BOOKCENTRE\Desktop\ssPyQt5_report_creation'
        file_name = '\\sas.txt'
        shutil.copyfile(source_path + file_name, dest_path + file_name)
        result = dest_path + '\\result.xlsx'
        return result
    except Exception as exc:
        print(exc)
        return False


def get_cc_count(pid, cam, date, start_time, end_time):
    try:
        def get_count_in_file(start_time, end_time):
            count = 0
            with open('exported_log.txt') as file:
                for line in file:
                    if 'Вход' in line:
                        time_in_line = re.findall(r'..:..:..', line)
                        time_in_line = datetime.datetime.strptime(
                            time_in_line[0], '%H:%M:%S')
                        if start_time < time_in_line < end_time:
                            count += 1
            return count

        # pid = input('Enter PID: ')
        # cam = input('Enter cam: ')
        # date = input('Enter date (yymmdd): ')
        start_time = datetime.datetime.strptime(
            start_time, '%H:%M:%S')
        end_time = datetime.datetime.strptime(
            end_time, '%H:%M:%S')
        final_count = 0
        local_path = r'C:\Users\Dorofeev.E.BOOKCENTRE\Desktop\ssPyQt5_report_creation\exported_log.txt'

        ftp = FTP()
        ftp.connect('ftp1', 21)
        print(ftp.login('clevercam', 'clevercam'))
        ftp.encoding = 'utf-8'
        ftp.cwd(f'/{pid}/{cam}/')

        files = ftp.nlst()  # получить названия всех файлов в директории
        # поиск файлов по дате
        matching_files = []
        for file in files:
            temp = re.findall(f'_{date}_', file)
            if temp:
                matching_files.append(file)

        print(matching_files)

        for file in matching_files:
            if os.path.exists(local_path):
                os.remove(local_path)

            local_file = open('exported_log.txt', 'wb')
            ftp.retrbinary(f'RETR {file}', local_file.write, 1024)

            local_file.close()
            final_count += get_count_in_file(start_time, end_time)
            os.remove(local_path)

        ftp.close()

        # print('Всего посетителей за указанный период:', final_count)
        return final_count
    except Exception as exc:
        print(exc)
        return False
    # create_db()
