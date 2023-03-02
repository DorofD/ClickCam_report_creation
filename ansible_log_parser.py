import logging


logging.basicConfig(level=logging.INFO,
                    filename="ansible_parser_log.txt", filemode="w")

sas = open('log')

count = 0
router = 'start '
address = '228'
for i in sas:
    if 'ok:' in i:
        # logging.info(f"{router[0:-2]}:comments:{count}")
        # logging.info(f"{router[0:-2]}:PPPoE:{count}")
        logging.info(f"{router[0:-2]}:DHCP:{count}:address:{address}")
        print(i)
        count = 0
        router = i
    # elif 'comment' in i:
    # elif 'pppoe' in i:
    elif 'address' in i:
        count += 1
        address = i
        print(i)
    # logging.info(f"{i}")
