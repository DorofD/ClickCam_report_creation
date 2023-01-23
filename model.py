import sqlite3 as sq
import openpyxl
import os
import shutil


def create_db():
    conn = sq.connect('database.db')
    cursor = conn.cursor()
    query = """CREATE TABLE IF NOT EXISTS contracts (
        id INTEGER NOT NULL UNIQUE, 
        pid INTEGER NOT NULL,
        shop_name TEXT NOT NULL,
        wan_type TEXT NOT NULL,
        ip TEXT,
        legal_entity TEXT NOT NULL,
        isp TEXT NOT NULL,
        contract TEXT,
        shop_address TEXT NOT NULL,
        sd_phone TEXT,
        sd_email TEXT,
        PRIMARY KEY ("id" AUTOINCREMENT)
    )
    """
    cursor.execute(query)

    query = """CREATE TABLE IF NOT EXISTS users (
        id INTEGER UNIQUE, 
        username TEXT NOT NULL UNIQUE,
        psw TEXT NOT NULL,
        user_type TEXT NOT NULL,
        auth_type TEXT NOT NULL,
        PRIMARY KEY ("id" AUTOINCREMENT)
    )
    """
    cursor.execute(query)
    conn.close()


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
    except:
        conn.close()
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
    if operator == 0:
        file_path = get_all_reports(operators[operator])
    else:
        file_path = get_one_report(operators[operator])
    print(operators[operator])
    try:
        source_path = r'\\operator4\c$\zDistr'
        dest_path = r'C:\Users\Dorofeev.E.BOOKCENTRE\Desktop\ssPyQt5_report_creation'
        file_name = '\\sas.txt'
        shutil.copyfile(source_path + file_name, dest_path + file_name)
        result = dest_path + '\\result.xlsx'
        return result
    except Exception as exc:
        print(exc)
        return False

# create_db()
