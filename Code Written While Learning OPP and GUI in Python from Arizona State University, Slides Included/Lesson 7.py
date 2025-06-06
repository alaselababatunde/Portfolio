from tkinter import *

root = Toplevel()
root.title('PythonGuides')


photo = PhotoImage(file='/Users/osburn/Desktop/smile.png')
photo = photo.subsample(2)
lbl = Label(root,image = photo)
lbl.image = photo
lbl.grid(column=0, row=3)

mainloop()
