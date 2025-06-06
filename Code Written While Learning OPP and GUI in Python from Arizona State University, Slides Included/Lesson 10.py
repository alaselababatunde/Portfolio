from tkinter import *

root = Tk()
root.geometry("200x220")
root.title("List Boxes")
frame = Frame(root)
frame.pack()

label = Label(root, text="A list of Car Parts.")
label.pack()

listbox = Listbox(root)  # Creats the Listbox widget
listbox.insert(1, "Breaks")  # adds items to the widget
listbox.insert(2, "Muffler")
listbox.insert(3, "Tires")
listbox.insert(4, "Windshield Wipers")
listbox.insert(5, "Head Lights")
listbox.pack()

root.mainloop()
