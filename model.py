import sqlite3 as sq
import openpyxl
import os
import shutil
from ftplib import FTP
import re
import datetime


def get_report(operator, date):
    operators_names = {
        'Оператор 1': 'Пак Алина',
        'Оператор 2': 'Багдасарова Ирина',
        'Оператор 3': 'Чинарева Александра',
        'Оператор 4': 'Клюев Михаил',
        'Оператор 5': 'Бугакова Татьяна'
    }
    operators = {
        0: ['operator11', 'operator2', 'operator33', 'operator4', 'operator5'],
        1: 'operator11',
        2: 'operator2',
        3: 'operator33',
        4: 'operator4',
        5: 'operator5',
    }
    try:
        # отчет на одного оператора
        if operator != 0:
            today = str(datetime.date.today())
            if os.path.exists(rf'C:\Users\Dorofeev.E.BOOKCENTRE\Desktop\ssPyQt5_report_creation\Оператор{operator} {date}.xlsx'):
                os.remove(
                    rf'C:\Users\Dorofeev.E.BOOKCENTRE\Desktop\ssPyQt5_report_creation\Оператор{operator} {date}.xlsx')
            filepath = rf'C:\Users\Dorofeev.E.BOOKCENTRE\Desktop\ssPyQt5_report_creation\Оператор{operator} {date}.xlsx'
            wb = openpyxl.Workbook()
            wb.save(filepath)
            # подключение листа Excel
            wb = openpyxl.load_workbook(f'Оператор{operator} {date}.xlsx')
            sheet = wb.active
            # загрузка БД
            source_path = rf'\\{operators[operator]}\c$\zDistr\!ssPyQt5\main'
            dest_path = rf'C:\Users\Dorofeev.E.BOOKCENTRE\Desktop\ssPyQt5_report_creation'
            file_name = '\\database.db'
            shutil.copyfile(source_path + file_name, dest_path + file_name)

            conn = sq.connect('database.db')
            cursor = conn.cursor()
            query = f"""
                SELECT * FROM notes
                WHERE date = '{date}'
            """
            cursor.execute(query)
            notes = cursor.fetchall()
            sheet[f'B{1}'].value = 'Дата'
            sheet[f'A{1}'].value = 'Оператор'
            sheet[f'C{1}'].value = 'Время МСК'
            sheet[f'D{1}'].value = 'Время местное'
            sheet[f'E{1}'].value = 'Магазин'
            sheet[f'F{1}'].value = 'Проход'
            sheet[f'G{1}'].value = 'Скриншот'
            sheet[f'I{1}'].value = 'Оператор'
            sheet[f'J{1}'].value = 'Время МСК'
            sheet[f'K{1}'].value = 'Магазин'
            sheet[f'L{1}'].value = 'Проход'
            sheet[f'M{1}'].value = 'Статус интервала'

            i = 2
            for note in notes:
                sheet[f'A{i}'].value = note[1]
                sheet[f'B{i}'].value = note[2]
                sheet[f'C{i}'].value = note[3][0:19]
                sheet[f'D{i}'].value = note[4][0:19]
                sheet[f'E{i}'].value = note[5]
                sheet[f'F{i}'].value = note[6]
                sheet[f'G{i}'].value = note[7]
                i += 1

            query = f"""
                SELECT * FROM intervals
                WHERE date = '{date}'
            """
            cursor.execute(query)
            notes = cursor.fetchall()
            for note in notes:
                print(note)

            i = 2
            for note in notes:
                sheet[f'I{i}'].value = note[0]
                sheet[f'J{i}'].value = note[1][0:19]
                sheet[f'K{i}'].value = note[2]
                sheet[f'L{i}'].value = note[3]
                sheet[f'M{i}'].value = note[4]

                i += 1

            wb.save(f'Оператор{operator} {date}.xlsx')
            conn.close()
            os.remove(
                rf'C:\Users\Dorofeev.E.BOOKCENTRE\Desktop\ssPyQt5_report_creation\database.db')
            result = rf'Оператор{operator} {date}.xlsx'
            return result

        # отчет на всех операторов
        else:
            if date:
                date = str(datetime.datetime.strptime(date, '%d-%m-%Y'))
            else:
                date = str(datetime.date.today())
            if os.path.exists(rf'C:\Users\Dorofeev.E.BOOKCENTRE\Desktop\ssPyQt5_report_creation\Все операторы {date}.xlsx'):
                os.remove(
                    rf'C:\Users\Dorofeev.E.BOOKCENTRE\Desktop\ssPyQt5_report_creation\Все операторы {date}.xlsx')
            filepath = rf'C:\Users\Dorofeev.E.BOOKCENTRE\Desktop\ssPyQt5_report_creation\Все операторы {date}.xlsx'
            wb = openpyxl.Workbook()
            wb.save(filepath)
            # подключение листа Excel
            wb = openpyxl.load_workbook(f'Все операторы {date}.xlsx')
            sheet = wb.active
            sheet[f'B{1}'].value = 'Дата'
            sheet[f'A{1}'].value = 'Оператор'
            sheet[f'C{1}'].value = 'Время МСК'
            sheet[f'D{1}'].value = 'Время местное'
            sheet[f'E{1}'].value = 'Магазин'
            sheet[f'F{1}'].value = 'Проход'
            sheet[f'G{1}'].value = 'Скриншот'
            sheet[f'I{1}'].value = 'Оператор'
            sheet[f'J{1}'].value = 'Дата'
            sheet[f'K{1}'].value = 'Время МСК'
            sheet[f'L{1}'].value = 'Время Местное'
            sheet[f'M{1}'].value = 'Магазин'
            sheet[f'N{1}'].value = 'Проход'
            sheet[f'O{1}'].value = 'Статус интервала'

            i = 2
            for operator in operators[0]:

                # загрузка БД
                source_path = rf'\\{operator}\c$\zDistr\!ssPyQt5\main'
                dest_path = rf'C:\Users\Dorofeev.E.BOOKCENTRE\Desktop\ssPyQt5_report_creation'
                file_name = '\\database.db'
                shutil.copyfile(source_path + file_name, dest_path + file_name)

                conn = sq.connect('database.db')
                cursor = conn.cursor()
                query = f"""
                    SELECT * FROM notes
                    WHERE date = '{date}'
                """
                cursor.execute(query)
                notes = cursor.fetchall()
                j = i
                for note in notes:
                    sheet[f'A{i}'].value = note[1]
                    sheet[f'B{i}'].value = note[2]
                    sheet[f'C{i}'].value = note[3][0:19]
                    sheet[f'D{i}'].value = note[4][0:19]
                    sheet[f'E{i}'].value = note[5]
                    sheet[f'F{i}'].value = note[6]
                    sheet[f'G{i}'].value = note[7]
                    i += 1

                query = f"""
                    SELECT * FROM intervals
                    WHERE date = '{date}'
                """
                cursor.execute(query)
                notes = cursor.fetchall()
                for note in notes:
                    print(note)

                for note in notes:
                    sheet[f'I{j}'].value = note[0]
                    sheet[f'J{j}'].value = note[1]
                    sheet[f'K{j}'].value = note[2][0:19]
                    sheet[f'L{j}'].value = note[3][0:19]
                    sheet[f'M{j}'].value = note[4]
                    sheet[f'N{j}'].value = note[5]
                    sheet[f'O{j}'].value = note[6]

                    j += 1

                conn.close()
                os.remove(
                    rf'C:\Users\Dorofeev.E.BOOKCENTRE\Desktop\ssPyQt5_report_creation\database.db')
            wb.save(f'Все операторы {date}.xlsx')
            result = rf'Все операторы {date}.xlsx'
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
