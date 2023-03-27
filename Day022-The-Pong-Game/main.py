from game import Pong

game = Pong()

while game.on:
    game.move_ball()
    game.detect_edges()
    game.detect_strike()
    game.detect_miss()

game.screen.exitonclick()
