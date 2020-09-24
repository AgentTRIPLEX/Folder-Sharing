import os
import network

def get_code():
    with open('code.txt', 'r') as w:
        return w.read().strip()

def update_folder(data, folder=os.getcwd()):
    original = os.getcwd()

    if folder != original:
        os.chdir(folder)

    for path, value in data:
        if value == None and path.strip() != '' and not os.path.exists(path):
            os.mkdir(path)
        else:
            directory = os.path.dirname(path)
            if directory.strip() != '' and not os.path.exists(directory):
                os.mkdir(directory)

            if path.strip() != '':
                try:
                    with open(path, 'wb') as w:
                        w.write(value)
                except:
                    pass

    if folder != original:
        os.chdir(original)

def handle_message(message):
    if message[0] == 'UPDATE':
        update_folder(message[1])
        print('Folder Update Complete!')
