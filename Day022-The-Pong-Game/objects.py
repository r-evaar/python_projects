from turtle import Turtle
from opt import OPT
from random import randint
from time import sleep
from math import sqrt


class Paddle(Turtle):

    def __init__(self, screen, side="right"):
        super().__init__()
        self.screen = screen
        self.shape("square")
        self.color("white")
        self.penup()
        self.width = OPT.paddle_w
        self.shapesize(stretch_len=OPT.paddle_h/OPT.paddle_w)
        self.setheading(90)

        assert side in ["right", "left"]
        sign = 1 if side == "right" else -1
        self.goto(sign * (OPT.width/2-OPT.paddle_o), 0)
        self.screen.update()

    def slide(self, direction):
        diff = self.ycor() + direction*OPT.sensitivity
        self.goto(self.xcor(), diff)
        self.screen.update()

    def bind_keys(self, keys):
        self.screen.onkeypress(lambda: self.slide(1), keys['up'])
        self.screen.onkeypress(lambda: self.slide(-1), keys['down'])

    def get_max_distance(self):
        s1 = self.width * self.shapesize()[0]/2
        s2 = self.width * self.shapesize()[1]/2
        return sqrt(s1**2 + s2**2)


class Ball(Turtle):

    def __init__(self, screen):
        super().__init__()
        self.screen = screen
        self.shape("circle")
        self.color("white")
        self.width = OPT.ball_r
        self.penup()
        self.screen.update()
        self.recenter()
        self.sleep = OPT.ball_speed

    def recenter(self):
        self.setpos(0, 0)
        init_angle = randint(0, 359)
        self.setheading(init_angle)
        self.screen.update()

    def step(self):
        self.forward(OPT.ball_step)
        sleep(1/self.sleep)
        self.screen.update()

    def detect_bounce(self):
        upper_hit = self.ycor() + self.width / 2 >= OPT.height / 2
        lower_hit = self.ycor() - self.width / 2 <= - OPT.height / 2

        if upper_hit or lower_hit:
            angle = -self.heading()
            if angle > 360:
                angle -= 360
            self.setheading(angle)
        self.screen.update()

