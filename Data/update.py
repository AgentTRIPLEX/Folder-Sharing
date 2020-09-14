# CONNECTED TO PROJECT FOLDER SHARING

import os
import network

def get_code():
    with open('code.txt', 'r') as w:
        return w.read().strip()

def update_folder(data):
    for path, value in data:
        if value == None:
            os.mkdir(path)
        else:
            directory = os.path.dirname(path)
            if directory != '' and not os.path.exists(directory):
                os.mkdir(directory)
            try:
                with open(path, 'wb') as w:
                    w.write(value)
            except:
                print('Folder Update Incomplete!')

def handle_message(message):
    if message[0] == 'UPDATE':
        update_folder(message[1])
        print('Folder Update Complete!')

if not os.path.exists('code.txt'):
    with open('code.txt', 'w') as w:
        w.write('')

if get_code() != '':
    print('You Are Updating Your Folder!')
    input('Press Enter To Continue')

    try:
        client = network.Client(handle_message, '172.104.169.112', 5555)
        client.send(['UPDATE', get_code()])
    except:
        print('Server Is Offline!')
        input('Press Enter To Exit!')
