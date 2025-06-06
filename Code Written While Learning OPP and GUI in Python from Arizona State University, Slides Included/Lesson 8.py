from tkinter import *
from tkinter import messagebox


def insert_Task():
    task = entry.get()
    if task != "":
        listbox.insert(END, task)
        entry.delete(0, "end")
    else:
        messagebox.showwarning("warning", "Please enter some task.")


def del_Task():
    listbox.delete(ANCHOR)


root = Tk()
root.geometry('500x450+500+200')
root.title('Simple List')
root.config(bg='green')
root.resizable(width=False, height=False)

frame = Frame(root)
frame.pack(pady=10)

listbox = Listbox(
    frame,
    width=28,
    height=8,
    font=('Times', 14),
    bd=0,
    highlightthickness=0,
    activestyle="none",

)
listbox.pack(side=LEFT, fill=BOTH)

task_list = [
    'Make my list'

]

for items in task_list:
    listbox.insert(END, items)

scroll = Scrollbar(frame)
scroll.pack(side=RIGHT, fill=BOTH)

listbox.config(yscrollcommand=scroll.set)
scroll.config(command=listbox.yview)

entry = Entry(
    root,
    font=('times', 14)
)

entry.pack(pady=20)

button_frame = Frame(root)
button_frame.pack(pady=20)

addTask_button = Button(
    button_frame,
    text='Add Task',
    font=('times 14'),
    padx=20,
    pady=10,
    command=insert_Task
)
addTask_button.pack(fill=BOTH, expand=True, side=LEFT)
delTask_button = Button(
    button_frame,
    text='Delete Task',
    padx=20,
    pady=10,
    command=del_Task
)
delTask_button.pack(fill=BOTH, expand=True, side=LEFT)

root.mainloop()
