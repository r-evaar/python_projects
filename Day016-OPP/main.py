from turtle import Turtle, Screen
from time import sleep

timmy = Turtle()
screen = Screen()

timmy.shape('turtle')
timmy.color('cyan')

print(screen.canvheight, screen.canvwidth)

w = screen.canvwidth
for i in range(100):
    step = -10 if (timmy.position()[0]-w) > 0 else 10
    timmy.forward(step)

screen.exitonclick()
