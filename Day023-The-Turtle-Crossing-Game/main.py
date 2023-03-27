from engine import CrossingGame
from turtle import Screen
from utils import OPT

screen = Screen()
game = CrossingGame(screen, OPT)

while not game.over:
    game.move_cars()
    game.detect_collision()
    game.update_level()
    # game.over = True

game.screen.exitonclick()
