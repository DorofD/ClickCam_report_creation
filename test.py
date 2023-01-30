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

# start_time = input()
# end_time = input()
# start_time = datetime.datetime.strptime(input(), '%H:%M:%S')
# end_time = datetime.datetime.strptime(input(), '%H:%M:%S')


# def get_count_in_file(start_time, end_time):
#     count = 0
#     with open('big_log.txt') as file:
#         for line in file:
#             if 'Вход' in line:
#                 time_in_line = re.findall(r'..:..:..', line)
#                 time_in_line = datetime.datetime.strptime(
#                     time_in_line[0], '%H:%M:%S')
#                 if start_time < time_in_line < end_time:
#                     count += 1
#     return count


# time_in_line = '21:02:55'


# start_time = datetime.datetime.strptime(start_time, '%H:%M:%S')
# end_time = datetime.datetime.strptime(end_time, '%H:%M:%S')
# time_in_line = datetime.datetime.strptime(time_in_line, '%H:%M:%S')

# print(get_count_in_file(start_time, end_time))

operators = {
    0: ['operator11', 'operator2', 'operator33', 'operator4', 'operator5'],
    1: 'operator11',
    2: 'operator2',
    3: 'operator33',
    4: 'operator4',
    5: 'operator5',
}

for operator in operators[0]:
    print(operator)
