from turtle import Turtle
from opt import OPT


class ScoreBoard(Turtle):

    def __init__(self, screen, pos):
        super().__init__()
        self.color("white")
        self.penup()
        self.hideturtle()
        self.goto(pos)
        self.screen = screen
        self.screen.update()

    def update(self, txt='', font=OPT.font):
        self.clear()
        self.write(txt, align='center', font=font)
        self.screen.update()
