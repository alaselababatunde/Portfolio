from tkinter import *


def button_pressed(event):
    var.set("Pressed at [ " + str(event.x) + ", " + str(event.y) + " ]")


def button_released(event):
    var.set("Released at [ " + str(event.x) + ", " + str(event.y) + " ]")


def enter_window(event):
    var.set("Mouse is in the window")


def exit_window(event):
    var.set("Mouse exited the window")


root = Tk()
root.title("Mouse Events")

frame = Frame(root, width=300, height=300)
frame.pack()

var = StringVar()
var.set("Mouse Events status will be displayed here.")
label = Label(root, textvariable=var)
label.pack(side=BOTTOM)

frame.bind("<Button-1>", button_pressed)
# Button 1 is the leftmost button, button 2 is the middle button (where available),
# and button 3 the rightmost button.
frame.bind("<ButtonRelease-1>", button_released)  # Button 1 was released.
frame.bind("<Enter>", enter_window)  # The mouse pointer entered the widget
frame.bind("<Leave>", exit_window)  # The mouse pointer exited the widget

root.mainloop()
