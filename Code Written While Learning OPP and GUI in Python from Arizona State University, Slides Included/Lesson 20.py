from turtle import *


def moveForward():
    forward(10)


def moveLeft():
    left(45)


def moveRight():
    right(45)


def leave():
    win.bye()


setup(400, 500)
win = Screen()
win.title("Event Handling!")
win.bgcolor("lightblue")
main = Turtle()

win.onkey(moveForward, "Up")
win.onkey(moveLeft, "Left")
win.onkey(moveRight, "Right")
win.onkey(leave, "q")
win.listen()
win.mainloop()
