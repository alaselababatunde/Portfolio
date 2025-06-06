from tkinter import *

root = Tk()
root.geometry("300x600")
root.title('Layouts')



label1 = Label(root, text="Welcome", bg="red", fg="white")
label1.pack()
label2 = Label(root, text="TO", bg="green", fg="black")
label2.pack()
label3 = Label(root, text="Python", bg="blue", fg="white")
label3.pack()
label4 = Label(root, text="")
label4.pack()
label1 = Label(root, text="Welcome", bg="red", fg="white")
label1.pack(fill=X)
label2 = Label(root, text="TO", bg="green", fg="black")
label2.pack(fill=X)
label3 = Label(root, text="Python", bg="blue", fg="white")
label3.pack(fill=X)
label4 = Label(root, text="")
label4.pack()

label1 = Label(root, text="Welcome", bg="red", fg="white")
label1.pack(fill=X,  padx=15)
label2 = Label(root, text="To", bg="green", fg="black")
label2.pack(fill=X, padx=15)
label3 = Label(root, text="Python", bg="blue", fg="white")
label3.pack(fill=X, padx=15)
label4 = Label(root, text="")
label4.pack()

label1 = Label(root, text="Welcome", bg="red", fg="white")
label1.pack(fill=X,  pady=15)
label2 = Label(root, text="To", bg="green", fg="black")
label2.pack(fill=X, pady=15)
label3 = Label(root, text="Python", bg="blue", fg="white")
label3.pack(fill=X, pady=15)
label4 = Label(root, text="")
label4.pack()


label1 = Label(root, text="Welcome", bg="red", fg="white")
label1.pack(fill=X,  pady=15, side=LEFT)
label2 = Label(root, text="To", bg="green", fg="black")
label2.pack(fill=X, pady=15, side=LEFT)
label3 = Label(root, text="Python", bg="blue", fg="white")
label3.pack(fill=X, pady=15, side=RIGHT)
label4 = Label(root, text="")
label4.pack()

#label1 = Label(root, text="Welcome", bg="red", fg="white").grid(row=1, column=0)
#label2 = Label(root, text="To", bg="green", fg="black").grid(row=1, column=1)
#label3 = Label(root, text="Python", bg="blue", fg="white").grid(row=1, column=2)


mainloop()
