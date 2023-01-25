from ftplib import FTP
import re
import datetime
import os


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


pid = input('Enter PID: ')
cam = input('Enter cam: ')
date = input('Enter date (yymmdd): ')
start_time = datetime.datetime.strptime(
    input('Enter start time (hh:mm:ss): '), '%H:%M:%S')
end_time = datetime.datetime.strptime(
    input('Enter end time (hh:mm:ss): '), '%H:%M:%S')
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

print('Всего посетителей за указанный период:', final_count)
