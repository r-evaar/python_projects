from random import randint, choice
from turtle import Turtle, Screen

timmy = Turtle()
screen = Screen()
screen.colormode(255)

timmy.shape("classic")
timmy.color("red")


def create_square(t, length):
    for i in range(4):
        t.forward(length)
        t.right(90)


def create_dash_line(t, length, lpp):
    toggle = False
    for i in range(round(length/lpp)):
        t.penup() if toggle else t.pendown()
        t.forward(lpp)
        toggle = not toggle
    t.pendown()


def random_color(t):
    t.color(tuple([randint(1, 255) for _ in range(3)]))


def create_shape(t, p, length):
    d = 360/p
    for i in range(p):
        t.right(d)
        t.forward(length)


def create_shapes(t, p, length):
    for i in range(3, p+1):
        random_color(t)
        create_shape(t, i, length)


def random_movement(t, length, n):
    t.pensize(10)
    t.speed(10)
    for _ in range(n):
        random_color(t)
        t.forward(length)
        angle = choice([0, 90, 180, 270])
        t.setheading(angle)
    t.pensize()
    t.speed()


def create_circles(t, r, n):
    angle = 360/n
    t.speed("fastest")
    heading = 0
    for _ in range(n):
        random_color(t)
        t.circle(r)
        t.setheading(heading)
        heading += angle
    t.speed()

# create_square(timmy, 100)
# timmy.right(180)
# create_dash_line(timmy, 100, 5)
#
# screen.reset()
# create_shapes(timmy, 10, 100)

# screen.reset()
# random_movement(timmy, 20, 200)

screen.reset()
create_circles(timmy, 100, 80)

screen.exitonclick()
