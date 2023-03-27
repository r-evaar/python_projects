from turtle import Turtle, Screen
from time import sleep

tim = Turtle()
screen = Screen()

keys = ["w", "s", "d", "a"]
functions = [Turtle.forward, Turtle.backward, Turtle.right, Turtle.left]

for i, key in enumerate(keys):
    screen.onkeypress(eval(f"lambda: functions[{i}](tim, 10)"), key)

def clear(): tim.clear(); tim.penup(); tim.home(); tim.pendown()

screen.onkeypress(clear, "c")
screen.listen()
screen.exitonclick()
