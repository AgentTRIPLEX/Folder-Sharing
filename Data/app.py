import share
import update
import network

from plyer import notification
import os
import tkinter
import tkinter.filedialog

class App:
    def __init__(self):
        self.window = tkinter.Tk()
        self.window.title('Folder Sharing')
        self.window.resizable(0,0)
        self.window.protocol('WM_DELETE_WINDOW', self.quit)

        try:
            self.client = network.Client(self.handle_message, '172.104.169.112', 5555)
        except:
            notification.notify(title='Server Offline', message="The Servers are Down! Please Try Again Later!", timeout=10)
            self.window.destroy()
            self.window.quit()
            return

        self.draw()

        self.window.mainloop()

    def draw(self):
        self.reset_window()
        tkinter.Button(self.window, text='Share', font=('Copperplate Gothic Bold', 30), width=20, fg='Red', bg='Black', command=lambda: self.code_panel(0)).grid(column=0, row=0)
        tkinter.Button(self.window, text='Update', font=('Copperplate Gothic Bold', 30), width=20, fg='Blue', bg='Black', command=lambda: self.code_panel(1)).grid(column=0, row=1)

    def reset_window(self):
        for child in self.window.winfo_children():
            child.destroy()

    def code_panel(self, mode):
        def submit():
            code = code_entry.get().strip()
            folder = tkinter.filedialog.askdirectory(parent=self.window, title='Directory To Share')

            with open('code.txt', 'w') as w:
                w.write(code)

            if os.path.exists(folder):
                self.loading_panel()

                if mode == 0:
                    self.client.send(['SHARE', [code, share.get_folder_data(folder)]])
                else:
                    self.client.send(['UPDATE', code])
                    self.folder = folder

        self.reset_window()
        code_entry = tkinter.Entry(self.window, width=30, font=('Times New Roman', 20))
        code_entry.grid(column=0, row=0, columnspan=2)
        tkinter.Button(self.window, text='Back', bg='Black', fg='Red', font=('Helvetica', 20), width=11, command=self.draw).grid(column=0, row=1)
        tkinter.Button(self.window, text='Submit', bg='Black', fg='Lime', font=('Helvetica', 20), width=15, command=submit).grid(column=1, row=1)

        if not os.path.exists('code.txt') or share.get_code() == '':
            code_entry.insert(0, 'Code Goes Here')
        else:
            code_entry.insert(0, share.get_code())

    def loading_panel(self):
        self.reset_window()
        tkinter.Label(self.window, text='Loading...', font=('Helvetica', 50), width=20, height=3, bg='Black', fg='Gold').pack()

    def handle_message(self, message):
        if message[0] == 'UPDATE':
            update.update_folder(message[1], self.folder)
            self.folder = None
            self.draw()

        elif message[0] == 'SHARED':
            self.draw()

    def quit(self):
        self.window.destroy()
        self.client.send(['QUIT'])
        self.client.close()
        self.window.quit()

if __name__ == '__main__':
    App()