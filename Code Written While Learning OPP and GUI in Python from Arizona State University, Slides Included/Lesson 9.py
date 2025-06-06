from tkinter import *
from tkinter import messagebox

root = Tk()
root.title('Dialog Boxes')
root.geometry('300x200')


def msg1():
    messagebox.showinfo('information', 'Please call Support.')
    messagebox.showerror('error', 'There was an error!')
    messagebox.showwarning('warning', 'This is a warning')
    messagebox.askquestion('Ask Question', 'Do you want to continue?')
    messagebox.askokcancel('Ok Cancel', 'Are You sure?')
    messagebox.askyesno('Yes|No', 'Do you want to proceed?')
    messagebox.askretrycancel('retry', 'Failed! want to try again?')

Button(root, text='Click Me', command=msg1).pack()

root.mainloop()

