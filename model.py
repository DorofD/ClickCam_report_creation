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
    print(operator)
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
    try:
        today = str(datetime.date.today())
        if os.path.exists(rf'C:\Users\Dorofeev.E.BOOKCENTRE\Desktop\ssPyQt5_report_creation\Оператор{operator} {today}.xlsx'):
            os.remove(
                rf'C:\Users\Dorofeev.E.BOOKCENTRE\Desktop\ssPyQt5_report_creation\Оператор{operator} {today}.xlsx')
        filepath = rf'C:\Users\Dorofeev.E.BOOKCENTRE\Desktop\ssPyQt5_report_creation\Оператор{operator} {today}.xlsx'
        wb = openpyxl.Workbook()
        wb.save(filepath)
        source_path = rf'\\operator5\c$\zDistr\!ssPyQt5\main'
        dest_path = rf'C:\Users\Dorofeev.E.BOOKCENTRE\Desktop\ssPyQt5_report_creation'
        file_name = '\\database.db'
        shutil.copyfile(source_path + file_name, dest_path + file_name)

        conn = sq.connect('database.db')
        cursor = conn.cursor()
        query = """
            SELECT * FROM notes
        """
        cursor.execute(query)
        notes = cursor.fetchall()

        if operator == 0:
            file_path = get_all_reports(operators[operator])

        else:
            for note in notes:
                print(note)
            # file_path = get_one_report(operators[operator])
        result = '228'
        return result
    except Exception as exc:
        print(exc)
        return False


def get_cc_count(pid, cam, date, start_time, end_time):
    try:
        date = str(date[4:] + date[2:4] + date[0:2])

        def get_count_in_file(start_time, end_time):
            with open('exported_log.txt') as file:
                entered = 0
                out = 0
                for line in file:
                    if 'Вход' in line:
                        time_in_line = re.findall(r'..:..:..', line)
                        time_in_line = datetime.datetime.strptime(
                            time_in_line[0], '%H:%M:%S')
                        if start_time < time_in_line < end_time:
                            entered += 1
                    if 'Выход' in line:
                        time_in_line = re.findall(r'..:..:..', line)
                        time_in_line = datetime.datetime.strptime(
                            time_in_line[0], '%H:%M:%S')
                        if start_time < time_in_line < end_time:
                            out += 1

            return [entered, out]

        # pid = input('Enter PID: ')
        # cam = input('Enter cam: ')
        # date = input('Enter date (yymmdd): ')
        start_time = datetime.datetime.strptime(
            start_time, '%H:%M:%S')
        end_time = datetime.datetime.strptime(
            end_time, '%H:%M:%S')
        final_entered = 0
        final_out = 0
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
            final_entered += get_count_in_file(start_time, end_time)[0]
            final_out += get_count_in_file(start_time, end_time)[1]
            os.remove(local_path)
        result = [final_entered, final_out]
        ftp.close()

        # print('Всего посетителей за указанный период:', final_count)
        return result
    except Exception as exc:
        print(exc)
        return False


# create_db()
# get_report(5)
