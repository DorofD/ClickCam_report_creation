import sqlite3 as sq
import openpyxl
import os
import shutil
from ftplib import FTP
import re
import datetime
from dotenv import load_dotenv
import urllib.request

dotenv_path = os.path.join(os.path.dirname(__file__), '.env')
if os.path.exists(dotenv_path):
    load_dotenv(dotenv_path)


COUNT_LOCAL_PATH = os.environ['COUNT_LOCAL_PATH']
PROJECT_LOCAL_PATH = os.environ['PROJECT_LOCAL_PATH']


def get_report(operator, date):
    operators_names = {
        'operator11': 'Пак Алина',
        'operator2': 'Багдасарова Ирина',
        'operator33': 'Чинарева Александра',
        'operator4': 'Клюев Михаил',
        'operator5': 'Бугакова Татьяна'
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
        # отчет на всех операторов
        if date:
            date = str(datetime.datetime.strptime(date, '%d-%m-%Y'))
        else:
            date = str(datetime.date.today())
        if os.path.exists(rf'{PROJECT_LOCAL_PATH}\Все операторы {date}.xlsx'):
            os.remove(
                rf'{PROJECT_LOCAL_PATH}\Все операторы {date}.xlsx')
        filepath = rf'{PROJECT_LOCAL_PATH}\Все операторы {date}.xlsx'
        wb = openpyxl.Workbook()
        wb.save(filepath)
        # подключение листа Excel
        wb = openpyxl.load_workbook(f'Все операторы {date}.xlsx')
        sheet = wb.active
        sheet[f'A{1}'].value = 'Оператор'
        sheet[f'B{1}'].value = 'ФИО'
        sheet[f'C{1}'].value = 'Дата'
        sheet[f'D{1}'].value = 'Время МСК'
        sheet[f'E{1}'].value = 'Время местное'
        sheet[f'F{1}'].value = 'Магазин'
        sheet[f'G{1}'].value = 'Проход'
        sheet[f'H{1}'].value = 'Скриншот'
        sheet[f'J{1}'].value = 'Оператор'
        sheet[f'K{1}'].value = 'Дата'
        sheet[f'L{1}'].value = 'Время МСК'
        sheet[f'M{1}'].value = 'Время Местное'
        sheet[f'N{1}'].value = 'Магазин'
        sheet[f'O{1}'].value = 'Проход'
        sheet[f'P{1}'].value = 'Статус интервала'

        i = 2
        for operator in operators[0]:

            # загрузка БД
            source_path = rf'\\{operator}\c$\zDistr\!ssPyQt5\main'
            dest_path = rf'{PROJECT_LOCAL_PATH}'
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
                sheet[f'B{i}'].value = operators_names[operator]
                sheet[f'C{i}'].value = note[2]
                sheet[f'D{i}'].value = note[3][0:19]
                sheet[f'E{i}'].value = note[4][0:19]
                sheet[f'F{i}'].value = note[5]
                sheet[f'G{i}'].value = note[6]
                sheet[f'H{i}'].value = note[7]
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
                sheet[f'J{j}'].value = note[0]
                sheet[f'K{j}'].value = note[1]
                sheet[f'L{j}'].value = note[2][0:19]
                sheet[f'M{j}'].value = note[3][0:19]
                sheet[f'N{j}'].value = note[4]
                sheet[f'O{j}'].value = note[5]
                sheet[f'P{j}'].value = note[6]

                j += 1

            conn.close()
            os.remove(
                rf'{PROJECT_LOCAL_PATH}\database.db')
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
            with open('exported_log.txt', mode='r', encoding='latin-1') as file:
                entered = 0
                out = 0
                for line in file:
                    if 'Âõîä' in line:  # Вход
                        time_in_line = re.findall(r'..:..:..', line)
                        time_in_line = datetime.datetime.strptime(
                            time_in_line[0], '%H:%M:%S')
                        if start_time < time_in_line < end_time:
                            entered += 1
                    if 'Âûõîä' in line:  # Выход
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
        # COUNT_LOCAL_PATH = r'{PROJECT_LOCAL_PATH}\exported_log.txt'

        ftp = FTP()
        ftp.connect('192.168.8.220', 21)
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
            if os.path.exists(COUNT_LOCAL_PATH):
                os.remove(COUNT_LOCAL_PATH)

            # local_file = open('exported_log.txt', 'wb')
            urllib.request.urlretrieve(
                f'ftp://clevercam:clevercam@192.168.8.220/{pid}/{cam}/{file}', 'exported_log.txt')
            # f'ftp://clevercam:clevercam@192.168.8.220/10/cam1/Log_230305_083748.txt', 'exported_log.txt')
            # ftp.retrbinary(f'{file}', local_file.write, 1024)
            # local_file.close()
            final_entered += get_count_in_file(start_time, end_time)[0]
            final_out += get_count_in_file(start_time, end_time)[1]
            # os.remove(COUNT_LOCAL_PATH)
        result = [final_entered, final_out]
        ftp.close()

        # print('Всего посетителей за указанный период:', final_count)
        return result
    except Exception as exc:
        print(exc)
        return False


# pid, cam, date, start_time, end_time
# print(get_cc_count('10', 'cam1', '200123', '10:00:00', '17:00:00'))

# create_db()
# get_report(5)
