from tkinter import *
root = Tk() #create the root window
root.geometry("400x500") #size of the window
#root.config(bg="black") #to change the background colour of the window
def write_message():#message for second button
    print("Hello, World")
def quit():#exit the window
    root.destroy()

#   create the button object with red text
button = Button(root, text = "QUIT", fg="red", command = root.quit)
button.pack(side=LEFT)
#create a second button object that diplays a message in a console
message = Button(root, text = "Welcome Message", fg="pink", command = write_message)
message.pack(side=RIGHT)

button2 = Button(root, text = "TOP", fg="blue")
button2.pack(side=TOP)

button3 = Button(root, text = "BOTTOM", fg="green")
button3.pack(side=BOTTOM)


root.mainloop()