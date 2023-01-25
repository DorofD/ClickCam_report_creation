import os
import time
import re
import datetime

# print(os.path.getctime('zalupa.txt'))
# print("created: %s" % time.ctime(os.path.getctime('zalupa.txt')))
# date = ''
# a = re.findall(r'_......_', f'_{date}_')
# print(a)
# if a:
#     print(1)

# # проверка регуляркой
# date = '201211'
# temp = re.findall(r'_......_', f'_{date}_')
# if temp:
#     print(temp)

# парсинг времени в файле
# with open('big_log.txt') as file:
#     for line in file:
#         if 'Вход' in line:
#             time_in_line = re.findall(r'..:..:..', line)
#             # print(time_in_line[0])
#             time_parts = [int(s) for s in time_in_line[0].split(':')]
#             print(time_parts)

# time_in_line = '21:02:55'
# time_parts = [int(s) for s in boba.split(':')]
# print(time_parts)
start_time = input()
end_time = input()
time_in_line = '21:02:55'

start_time = datetime.datetime.strptime(start_time, '%H:%M:%S')
end_time = datetime.datetime.strptime(end_time, '%H:%M:%S')
time_in_line = datetime.datetime.strptime(time_in_line, '%H:%M:%S')

print(start_time < time_in_line < end_time)
