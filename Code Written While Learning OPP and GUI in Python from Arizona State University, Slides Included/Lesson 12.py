from tkinter import *

root = Tk()
root.geometry("400x300")
root.title('Menu')

# Creating Menubar
menubar = Menu(root)

# Adding File Menu and commands
file = Menu(menubar, tearoff=0)
menubar.add_cascade(label='File', menu=file)
file.add_command(label='New File', command=None)
file.add_command(label='Open...', command=None)
file.add_command(label='Save', command=None)
file.add_separator()
file.add_command(label='Exit', command=root.destroy)

# Adding Help Menu
helpInfo = Menu(menubar, tearoff=0)
menubar.add_cascade(label='Contact Help', menu=helpInfo)
helpInfo.add_command(label='Help Lessons', command=None)
helpInfo.add_separator()
helpInfo.add_command(label='About', command=None)

# display Menu
root.config(menu=menubar)
mainloop()
