from turtle import *


def draw_bar(turtle1, height, colorBars):
    turtle1.fillcolor(colorBars)
    turtle1.begin_fill()
    turtle1.left(90)
    turtle1.forward(height)
    turtle1.write(str(height))
    turtle1.right(90)
    turtle1.forward(40)
    turtle1.right(90)
    turtle1.forward(height)
    turtle1.left(90)
    turtle1.end_fill()


yaxis = [30, 100, 120, 60, 135, 200, 110]
colors = ["red", "brown", "blue", "green",
          "cyan", "yellow", "gray"]

maxheight = max(yaxis)
numberbars = len(yaxis)
bordr = 10

screen = Screen()
screen.setworldcoordinates(0 - bordr, 0 - bordr,
                           40 * numberbars + bordr,
                           maxheight + bordr)

turtle1 = Turtle()
turtle1.pensize(3)

for x in range(len(yaxis)):
    draw_bar(turtle1, yaxis[x],
             colors[x])

screen.exitonclick()
