from random import randint


class OPT:

    SCREEN_W        = 600
    SCREEN_H        = 400
    CAR_H           = 20
    CAR_W           = 30
    N_CARS          = 10
    SQUISH          = 5
    MIN_SPEED       = 100
    MAX_SPEED       = 1000
    SPEED_INC       = 5


def random_color():
    return tuple(randint(0, 255) for _ in range(3))

