from tkinter import *

root = Tk()
root.geometry("400x300")
root.title('Frames')

#Builds the frame
frame = Frame(root)
frame.pack()

#Setup the different Frame sides
leftframe = Frame(root)
leftframe.pack(side=LEFT)
rightframe = Frame(root)
rightframe.pack(side=RIGHT)
topframe = Frame(root)
topframe.pack(side = TOP)
bottomframe = Frame(root)
bottomframe.pack(side = BOTTOM)


#Assigning the buttons to the different locations
button1 = Button(topframe, text="Button 1")
button1.pack(side=LEFT)

button2 = Button(bottomframe, text="Button 2")
button2.pack(side=RIGHT)

button3 = Button(rightframe, text="Button 3")
button3.pack(side=LEFT)

button4 = Button(leftframe, text="Button 4",)
button4.pack(side=RIGHT)

#Creates a Labeld Frame
labelFrame = LabelFrame(root, text="Fruit")
label1 = Label(labelFrame, text="Apples")
label1.grid(row=0, column=0)
label2 = Label(labelFrame, text="Oranges")
label2.grid(row=1, column=0)
label2 = Label(labelFrame, text="Bannanas")
label2.grid(row=2, column=0)
label2 = Label(labelFrame, text="Strawberries")
label2.grid(row=3, column=0)
#To display the frame
labelFrame.pack(padx=5, pady=5, ipadx=5, ipady=5)

mainloop()

