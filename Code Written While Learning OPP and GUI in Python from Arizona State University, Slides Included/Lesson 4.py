from tkinter import *
root = Tk() #create the root window
root.geometry("400x500") #size of the window
label1 = Label(root, text= "Welcome to GUI's in python") #create a label with words
label2 = Label(root, text = "Python is amazing!!!", font=("Helvitica", 14))
label1.config(fg = "green")
label1.pack()#put the label into the window
label2.pack()
root.mainloop() #start the event loop