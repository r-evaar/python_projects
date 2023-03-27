from turtle import Screen
from opt import OPT
from objects import Paddle, Ball
from scoreBoard import ScoreBoard


class Pong:

    def __init__(self):
        self.on = True
        self.screen = Screen()
        self.screen.setup(width=OPT.width, height=OPT.height)
        self.screen.bgcolor("black")
        self.screen.title("Pong")

        self.left_score = 0
        self.right_score = 0

        self.screen.tracer(0)
        self.setup_paddles()
        self.ball = Ball(self.screen)
        self.setup_scores()

        self.right_strike, self.left_strike = [False, False]

        self.screen.listen()

    def setup_scores(self):
        xr = int(self.screen.canvwidth * 0.75*0.5)
        xl = - xr
        y = int(self.screen.canvheight * 0.5)

        self.left_board = ScoreBoard(self.screen, (xl, y))
        self.right_board = ScoreBoard(self.screen, (xr, y))

        self.left_board.update(f"{self.left_score}")
        self.right_board.update(f"{self.right_score}")

    def setup_paddles(self):

        self.right_paddle = Paddle(self.screen, side="right")
        self.right_paddle.bind_keys({"up": "Up", "down": "Down"})
        self.left_paddle = Paddle(self.screen, side="left")
        self.left_paddle.bind_keys({"up": "w", "down": "s"})
        self.paddles = [self.left_paddle, self.right_paddle]

    def move_ball(self):
        self.ball.step()
        self.ball.detect_bounce()

    def detect_edges(self):
        rp = self.right_paddle
        lp = self.left_paddle

        right_paddle_distance = rp.get_max_distance()
        left_paddle_distance = lp.get_max_distance()

        right_line = rp.xcor() - rp.width
        left_line = lp.xcor() + lp.width

        radius = self.ball.width / 2

        ball_in_right_range = self.ball.distance(self.right_paddle) - (right_paddle_distance + radius) < 0
        ball_in_left_range = self.ball.distance(self.left_paddle) - (left_paddle_distance + radius) < 0

        self.lines, self.ball_in_range = \
            {'left': left_line, 'right': right_line}, \
            {'left': ball_in_left_range, 'right': ball_in_right_range}

    def detect_strike(self):
        assert hasattr(self, 'lines'), "@detect_edge method must be called first"

        a = self.ball.heading()

        if self.ball_in_range['right']:
            self.right_strike = self.ball.xcor() >= self.lines['right'] and (a < 90 or a > 270)

        if self.ball_in_range['left']:
            self.left_strike = self.ball.xcor() <= self.lines['left'] and 90 < a < 270

        if self.right_strike:
            from_down = True if a < 90 else False
            if from_down:
                theta = 90 - a
                a += 2 * theta
            else:
                theta = a - 270
                a -= 2 * theta

            self.ball.setheading(a)
            self.right_strike = False

        if self.left_strike:
            from_down = True if a < 180 else False
            if from_down:
                theta = a - 90
                a -= 2 * theta
            else:
                theta = 270 - a
                a += 2 * theta

            self.ball.setheading(a)
            self.left_strike = False

        self.screen.update()

    def detect_miss(self):
        lim = self.screen.window_width()/2
        right_miss = self.ball.xcor() > lim
        left_miss = self.ball.xcor() < -lim

        if right_miss or left_miss:
            self.ball.recenter()
            self.ball.sleep /= 0.8

        if right_miss:
            self.left_score += 1
            self.left_board.update(f"{self.left_score}")

        if left_miss:
            self.right_score += 1
            self.right_board.update(f"{self.right_score}")



