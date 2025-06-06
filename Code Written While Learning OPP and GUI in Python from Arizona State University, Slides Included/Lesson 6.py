from tkinter import *

from netaddr.strategy.ipv6 import width

root = Tk() #create the root window
root.geometry("400x500") #size of the window
root.title("TextBoxes")
root.config(bg="black")

def insert_text():
    user_input = textField1.get("1.0", END) #read from text box t1
    textField2.insert(END, user_input) #read from text box t2

user_input = StringVar()#declare a string variable

label1 = Label(root, text="what is your name?", width = 15) #crate a label
label1.grid(row=1,column=1) #location onn the window

textField1 = Text(root, height=1, width=16, bg="yellow") #create a text box
textField1.grid(row=1,column=2) #location onn the window

b1 = Button(root, text="update", width=10, bg="red", command = lambda: insert_text()) #create a button
b1.grid(row=2,column=2) #location onn the window

textField2 = Text(root, height=1, width=15, bg="pink") #added one textbox to read
textField2.grid(row=3,column=2) #location onn the wind

root.mainloop()