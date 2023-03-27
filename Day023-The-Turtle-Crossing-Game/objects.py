from turtle import Turtle
from utils import random_color
from random import randint
from time import time


class Object(Turtle):

    def __init__(self, screen, opt):
        super().__init__()
        self.penup()
        self.screen = screen
        self.OPT = opt
        self.copied = False


class Car(Object):

    def __init__(self, screen, opt, y):
        super().__init__(screen, opt)
        self.shape('square')
        self.width = self.OPT.CAR_W
        self.shapesize(self.OPT.CAR_H/self.width, 1)
        self.sety(y)
        self.start()
        self.vel = self.add_speed()
        self.setheading(180)

    def start(self):
        self.setx(self.screen.canvwidth/2)
        self.color(random_color())
        self.t = time()
        self.screen.update()

    def add_speed(self):
        factor = randint(1, 5)
        diff = self.OPT.MAX_SPEED - self.OPT.MIN_SPEED
        return self.OPT.MIN_SPEED + diff * factor/5

    def copy(self):
        new_obj = Car(self.screen, self.OPT, self.ycor())
        new_obj.vel = self.vel
        return new_obj
