import os
import time
import re

# print(os.path.getctime('zalupa.txt'))
# print("created: %s" % time.ctime(os.path.getctime('zalupa.txt')))
# date = ''
# a = re.findall(r'_......_', f'_{date}_')
# print(a)
# if a:
#     print(1)

date = '201211'
temp = re.findall(r'_......_', f'_{date}_')
if temp:
    print(temp)
