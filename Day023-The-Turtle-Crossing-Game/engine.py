from objects import Car
from time import time
from random import random


class CrossingGame():

    def __init__(self, screen, opts):

        self.OPT = opts

        self.screen = self.initialize_screen(screen)
        self.over = False
        self.lvl = 0

        self.cars = self.__initialize_car_col()

    def initialize_screen(self, screen):
        screen.bgcolor("white")
        screen.canvwidth = self.OPT.SCREEN_W
        screen.canvheight = self.OPT.SCREEN_H
        screen.setup(self.OPT.SCREEN_W, self.OPT.SCREEN_H)
        screen.tracer(0)
        screen.colormode(255)
        return screen

    def __initialize_car_col(self):
        spacing = self.screen.canvheight/(self.OPT.N_CARS+1) - self.OPT.SQUISH
        start = -self.screen.canvheight/2 + spacing + self.OPT.SQUISH * self.OPT.N_CARS
        cars = [Car(self.screen, self.OPT, start+i*spacing)
                for i in range(self.OPT.N_CARS)]
        return cars

    def move_cars(self):
        x = self.screen.canvwidth/2
        for i, car in enumerate(self.cars):
            speed = car.vel + self.lvl*self.OPT.SPEED_INC
            wait = 20/speed
            if time() - car.t > wait:
                car.forward(6)
                car.t = time()
            self.screen.update()

            if car.xcor() <= x*0.2*random() and not car.copied:
                new_car = car.copy()
                car.copied = True
                new_car.setx(x)
                self.cars += [new_car]

            if car.xcor() <= -x-self.OPT.CAR_W:
                car.hideturtle()
                del car
                del self.cars[i]

        print(len(self.cars))

    def detect_collision(self):
        pass

    def update_level(self):
        pass

