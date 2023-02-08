import os
import logging
import openpyxl
from pythonping import ping

logging.basicConfig(level=logging.INFO, filename="ping_log.txt", filemode="w")


# подключение листа Excel
wb = openpyxl.load_workbook(f'ping.xlsx')
sheet = wb.active

for i in range(1, sheet.max_row + 1):
    try:
        computer = sheet[f'A{i}'].value
        response = ping(computer, count=4, verbose=True)
        logging.info(f'LOSS:{response.packet_loss}:{computer}')
    except Exception as exc:
        print(exc)
        logging.error(f'{computer}')
