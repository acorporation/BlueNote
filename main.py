__author__ = 'Aarav Dave'
# © BlueNote 2021 Aarav Dave


from tkinter import *
from tkinter.filedialog import asksaveasfilename
from tkinter.filedialog import askopenfile
from tkinter import colorchooser
from tkinter import font
import os, subprocess


def select(event=None):
    document.tag_add(SEL, 1.0, END)
    return 'break'


def save(event=None):
    global file_name
    if not file_name:
        name = asksaveasfilename(
            defaultextension='*.blue',
            filetypes=files
        )
    else:
        name = file_name
    if name:
        file_name = name
        content = document.get(1.0, END)
        with open(file_name, 'w') as file:
            file.write(content)
            window.title(f'BlueNote - {os.path.basename(file_name)}')


def open_file(event=None):
    global file_name
    document.delete('1.0', END)
    file_name = askopenfile(defaultextension='*.blue', filetypes=files).name
    if file_name:
        document.insert('1.0', open(file_name, 'r').read())
        window.title(f'BlueNote - {os.path.basename(file_name)}')


def copy(event=None):
    document.event_generate('<<Copy>>')


def paste(event=None):
    document.event_generate('<<Paste>>')


def cut(event=None):
    document.event_generate('<<Cut>>')


def font_change(event=None):
    global current_font
    current_font = (current_choose_font.get(), current_choose_font_size.get())
    document.config(font=current_font)


def do_popup(event):
    popup.tk_popup(event.x_root, event.y_root)


def bold(event=None):
    bold_font = font.Font(document, document.cget('font'))
    bold_font.configure(weight='bold')
    document.tag_configure('bold', font=bold_font)
    if 'bold' in document.tag_names('sel.first'):
        document.tag_remove('bold', 'sel.first', 'sel.last')
    else:
        document.tag_add('bold', 'sel.first', 'sel.last')


def italics(event=None):
    color_font = font.Font(document, document.cget('font'))
    color_font.config(slant='italic')
    document.tag_config('italics', font=color_font)
    if 'italics' in document.tag_names('sel.first'):
        document.tag_remove('italics', 'sel.first', 'sel.last')
    else:
        document.tag_add('italics', 'sel.first', 'sel.last')


def color_text(event=None):
    color = colorchooser.askcolor()[1]
    if color:
        italics_font = font.Font(document, document.cget('font'))
        document.tag_config('colored', font=italics_font, foreground=color)
        document.tag_add('colored', 'sel.first', 'sel.last')


def print_file(event=None):
    lpr = subprocess.Popen("/usr/bin/lpr", stdin=subprocess.PIPE)
    lpr.stdin.write(document.get(1.0, END).encode('utf-8'))


window = Tk()
window.geometry('1000x700')
window.title('BlueNote - untitled')
window.iconphoto(False, PhotoImage(file='512.png'))

file_name = None
current_font = ('Avenir', 20)
files = [('BlueNote Document', '*.blue')]

document = Text(window, wrap='word', undo=True)
window.bind('<Command-b>', bold)
window.bind('<Command-i>', italics)

window.bind('<Command-s>', save)
window.bind('<Command-o>', open_file)

menu_bar = Menu(window)
file_menu = Menu(menu_bar, tearoff=0)
file_menu.add_command(label='Open', command=open_file, accelerator='Command+O')
file_menu.add_command(label='Save', command=save, accelerator='Command+S')
file_menu.add_command(label='Print', command=print_file, accelerator='Command+P')
file_menu.add_separator()
file_menu.add_command(label='Quit', command=window.destroy, accelerator='Command+Q')
menu_bar.add_cascade(label='File', menu=file_menu)

edit_menu = Menu(menu_bar, tearoff=0)
edit_menu.add_command(label='Copy', command=copy, accelerator='Command+C')
edit_menu.add_command(label='Cut', command=cut, accelerator='Command+X')
edit_menu.add_command(label='Paste', command=paste, accelerator='Command+V')
edit_menu.add_separator()
edit_menu.add_command(label='Select All', command=select, accelerator='Command+A')
edit_menu.add_separator()
edit_menu.add_command(label='Bold', command=bold, accelerator='Command+B')
edit_menu.add_command(label='Italicize', command=italics, accelerator='Command+I')
edit_menu.add_command(label='Color', command=color_text)
menu_bar.add_cascade(label='Edit', menu=edit_menu)

current_choose_font = StringVar(window, 'Avenir')
choose_font = OptionMenu(window, current_choose_font, *'Avenir, Helvetica, Futura, Andale Mono Regular, Annai MN Regular, Charter, Cochin, Comic Sans MS'.split(', '), command=font_change)
choose_font.place(x=0, y=0, width=250, height=25)

current_choose_font_size = StringVar(window, 20)
choose_font_size = OptionMenu(window, current_choose_font_size, *[8, 9, 10, 11, 12, 13, 16, 18, 20, 24, 30, 36], command=font_change)
choose_font_size.place(x=250, y=0, width=50, height=25)

bold_button_font = font.Font(weight='bold')
bold_button = Button(window, text='B', command=bold, font=bold_button_font)
bold_button.place(x=300, y=0, width=50, height=25)

italics_button_font = font.Font(slant='italic')
italics_button = Button(window, text='I', command=italics, font=italics_button_font)
italics_button.place(x=350, y=0, width=50, height=25)

color_button = Button(window, text='A', command=color_text)
color_button.place(x=400, y=0, width=50, height=25)

popup = Menu(window, tearoff=0)
popup.add_command(label='Copy', command=copy)
popup.add_command(label='Cut', command=cut)
popup.add_command(label='Paste', command=paste)
popup.add_separator()
popup.add_command(label='Color', command=color_text)
window.bind('<Button-2>', do_popup)

document.config(font=current_font)
document.place(x=0, y=25, width=1000, height=675)
window.config(menu=menu_bar)
window.mainloop()
