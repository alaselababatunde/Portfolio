from turtle import *

# for turtle shape
shape("turtle")


def makeSquare():
    color('red', 'yellow')
    begin_fill()
    for i in range(4):
        pensize(4)
        forward(100)
        left(90)
    end_fill()


def makeSquare2():
    for i in range(4):
        pensize(4)
        forward(100)
        left(90)


def spiral():
    pensize(2)
    for i in range(18):
        makeSquare2()
        left(20)


def line():
    pencolor('blue')
    forward(200)


def cir():
    pencolor('green')
    circle(60)


makeSquare()
penup()
setposition(-200, 0)
pendown()
spiral()
penup()
setposition(0, 200)
pendown()
line()
penup()
setposition(0, -200)
pendown()
cir()

done()
