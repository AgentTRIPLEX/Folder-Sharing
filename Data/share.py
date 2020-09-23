# CONNECTED TO PROJECT FOLDER SHARING

import os
import network

def get_short_directory(full_directory):
    directories = full_directory.split(os.sep)
    for _ in range(len(os.getcwd().split(os.sep))):
        directories.pop(0)
    return os.sep.join(directories)

def get_code():
    with open('code.txt', 'r') as w:
        return w.read().strip()

def get_filename():
    a = os.getcwd().split(os.sep)
    return a[len(a) - 1]

def read_path(path):
    with open(path, 'rb') as w:
        return w.read()

def get_folder_data(path=os.getcwd()):
    original = os.getcwd()

    if path != original:
        os.chdir(path)

    data = []

    for full_directory, _, files in os.walk(os.getcwd()):
        directory = get_short_directory(full_directory)
        path = None

        for file in files:
            path = os.path.join(directory, file)
            data.append([path, read_path(path)])

        if path == None:
            data.append([directory, None])

    if path != original:
        os.chdir(original)

    return data

def handle_message(message):
    if message[0] == 'SHARE':
        print('Folder Share Complete!')

if not os.path.exists('code.txt'):
    with open('code.txt', 'w') as w:
        w.write('')

if __name__ == '__main__' and get_code() != '':
    print('You Are Updating Your Server Data!')
    input('Press Enter To Continue')

    try:
        client = network.Client(handle_message, '172.104.169.112', 5555)
        client.send(['SHARE', [get_code(), get_folder_data()]])
    except:
        print('Server Is Offline')
        input('Press Enter To Exit!')
