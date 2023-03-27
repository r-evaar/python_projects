import colorgram
from turtle import Turtle, Screen
from random import choice

timmy = Turtle()
screen = Screen()
screen.colormode(255)

colors = colorgram.extract('./img.jpg', 10)
colors = [(color.rgb.r, color.rgb.g, color.rgb.b) for color in colors]


def create_circle(t, r):
    t.pendown()
    t.dot(r, choice(colors))
    t.penup()


def create_line(t, r, space, length):
    x = t.xcor()
    for _ in range(length):
        create_circle(t, r)
        x += space
        t.setx(x)


def create_painting(t, r, space, length):
    t.hideturtle()
    t.speed("fastest")
    t.penup()
    t.setpos(-screen.canvwidth*0.9, -screen.canvheight*0.9)
    y = t.ycor()
    x = t.xcor()
    for _ in range(length):
        create_line(t, r, space, length)
        y += space
        t.setpos(x, y)
    t.speed()
    t.pendown()


create_painting(timmy, 25, 60, 10)
screen.exitonclick()
