from ftplib import FTP

# i = 0
# with open('log.txt', 'r') as file:
#     for line in file:
#         if 'Вход' in line:
#             i += 1
# print(i)


def writeFunc(s):
    print("Read: " + s)


ftp = FTP()
ftp.connect('ftp1', 21)
print(ftp.login('clevercam', 'clevercam'))
ftp.encoding = 'utf-8'
ftp.cwd('/10/cam1/')
my_file = open('zalupa.txt', 'wb')
ftp.retrbinary('RETR Log_201014_202517.txt', my_file.write, 1024)
# ftp.retrlines('LIST')
my_file.close()


# sas = ftp.retrbinary(f'RETR /10/cam1/Log_201014_202517.txt', writeFunc)
ftp.close()
