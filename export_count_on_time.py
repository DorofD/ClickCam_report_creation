from ftplib import FTP
import re

# i = 0
# with open('log.txt', 'r') as file:
#     for line in file:
#         if 'Вход' in line:
#             i += 1
# print(i)


ftp = FTP()
ftp.connect('ftp1', 21)
print(ftp.login('clevercam', 'clevercam'))
ftp.encoding = 'utf-8'
ftp.cwd('/10/cam1/')
# my_file = open('zalupa.txt', 'wb')
# ftp.retrbinary('RETR Log_201014_202517.txt', my_file.write, 1024)
# ftp.retrlines('LIST')
# my_file.close()

files = ftp.nlst()  # получить названия всех файлов в директории


# поиск файлов по дате
date = '220410'
matching_files = []
for file in files:
    temp = re.findall(f'_{date}_', file)
    if temp:
        matching_files.append(file)


print(matching_files)


# sas = ftp.retrbinary(f'RETR /10/cam1/Log_201014_202517.txt', writeFunc)
ftp.close()


def get_number_of_visitors():
    pass
