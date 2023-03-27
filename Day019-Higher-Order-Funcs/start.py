from turtle import Turtle, Screen

tim = Turtle()
screen = Screen()
screen.listen()

screen.onkey(key="space", fun=lambda: tim.forward(10))
screen.exitonclick()
