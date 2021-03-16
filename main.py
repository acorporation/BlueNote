from tkinter import *
from tkinter import filedialog
import os


def update_file():
    if file.name != 'blank.txt':
        update = open(file.name, 'w')
        update.write(open_file.text.get('1.0', 'end-1c'))


def open_file():
    global file
    chosen = filedialog.askopenfilenames(
        parent=window,
        initialdir='/Users/',
        initialfile='tmp',
        filetypes=[
            ("TXT", "*.txt"),
            ("PY", "*.py")])
    file = open(chosen[-1], 'r')
    window.title(f'BlueNote - {file.name}')

    open_file.text = Text(window, width=1000, height=750, bg='#000219', fg='#fcfcfc')
    open_file.text.insert(END, file.read())
    open_file.text.config(highlightbackground='#12182B')
    open_file.text.place(x=0, y=50)


def new_file():
    global file
    file = open('untitled', 'w')
    window.title(f'BlueNote - {file.name}')

    open_file.text = Text(window, width=1000, height=750, bg='#000219', fg='#fcfcfc')
    open_file.text.insert(END, file.read())
    open_file.text.config(highlightbackground='#12182B')
    open_file.text.place(x=0, y=50)


tabs = []
file = open('blank.txt', 'r')
current = 0

window = Tk()
window.geometry('1000x800')
window.title('BlueNote')

menu = Menu(window)
filemenu = Menu(menu, tearoff=0)
filemenu.add_command(label='New File', command=new_file)
filemenu.add_command(label='Save', command=update_file)
filemenu.add_command(label='Open', command=open_file)
menu.add_cascade(label="File", menu=filemenu)

canvas = Canvas(window, width=1000, height=800, bg='#000533')
canvas.config(highlightbackground='#000533')
canvas.place(x=0, y=0)
canvas.create_text(500, 400, text='Press \'File\' and \'Open\' to get started.', fill='#fcfcfc')

window.configure(menu=menu, bg='#000533')
window.mainloop()
