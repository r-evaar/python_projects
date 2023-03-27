from turtle import Turtle
from time import sleep
from random import randint

HEAD_COLOR = (227, 192, 77)
BODY_COLORS = [(148, 7, 230), (0, 189, 189)]
DELAY = 0.1
OFFSET = 4
BLOCK_W = 20
FONT = ('Righteous', 14, 'normal')


# noinspection PyAttributeOutsideInit
class Snake:

    def __init__(self, screen, difficulty="easy", length=3):

        screen.colormode(255)
        screen.tracer(0)  # Turn off animation
        self.screen = screen
        self.screen.listen()

        self.colorToggle = False
        self.init_body(length)

        self.set_difficulty(difficulty)
        self.setup_control()

        self.game_over = False
        self.first_moved = False

    def block(self):
        block = Turtle()
        block.shape("circle")

        prev_block = self.body[-1]
        if prev_block is None:
            block.color(HEAD_COLOR)
            x, y = [-OFFSET, OFFSET]
        else:
            self.colorToggle = not self.colorToggle
            i = 0 if self.colorToggle else 1
            block.color(BODY_COLORS[i])

            x, y = prev_block.pos()
            head = prev_block.heading()
            if head == 0:
                x -= BLOCK_W
            elif head == 90:
                y -= BLOCK_W
            elif head == 180:
                x += BLOCK_W
            elif head == 270:
                y += BLOCK_W
            else:
                raise f"Invalid value for a Turtle object heading: {head}"

        block.penup()
        block.speed(0)
        block.setpos(x, y)

        return block

    def init_body(self, length):
        self.body = [None]
        for _ in range(length):
            self.grow()
        del self.body[0]
        self.first = self.body[0]

    def grow(self):
        self.body += [self.block()]

    def set_difficulty(self, difficulty):
        self.delay = DELAY
        options = ["easy", "medium", "hard"]
        assert difficulty in options, f"Unknown difficulty '{difficulty}'"\
                                          f". Please select one of the following: {options}"
        divisor = options.index(difficulty)+1
        self.delay /= divisor

    def setup_control(self):

        def head(block, direction):
            if abs(block.heading() - direction) in [0, 180] or not self.first_moved:
                pass
            else:
                block.setheading(direction)
            self.first_moved = False

        self.screen.onkeypress(lambda: head(self.first, 0),      "Right")
        self.screen.onkeypress(lambda: head(self.first, 180),    "Left")
        self.screen.onkeypress(lambda: head(self.first, 90),     "Up")
        self.screen.onkeypress(lambda: head(self.first, 270),    "Down")

    def move_snake(self):

        for i in range(len(self.body)-1, 0, -1):
            front = self.body[i-1]
            block = self.body[i]
            block.setpos(front.pos())

        self.first.forward(BLOCK_W)

        xMax = int(self.screen.window_width()/2)
        yMax = int(self.screen.window_height()/2)
        if \
                self.first.xcor() >= xMax-OFFSET or \
                self.first.xcor() <= -xMax+OFFSET or \
                self.first.ycor() >= yMax-OFFSET or \
                self.first.ycor() <= -yMax+OFFSET or \
                self.collision():

            self.game_over = True

        self.screen.update()
        self.first_moved = True
        sleep(self.delay)

    def collision(self, target=None):
        recolor = False
        if not target:
            target = self.first
            recolor = True

        for block in self.body[1:]:
            if block.distance(target) < BLOCK_W/2:
                if recolor:
                    block.color("red")
                return True
        return False


class Food(Turtle):

    def __init__(self, screen):
        super().__init__()
        self.shape("circle")
        self.penup()
        self.shapesize(stretch_len=0.5, stretch_wid=0.5)
        self.color("red")
        self.speed(0)
        self.screen = screen
        self.refresh()

    def refresh(self, avoid=None):
        x, y = [int(a / 2) - BLOCK_W for a in [self.screen.canvwidth, self.screen.canvheight]]
        x, y = [randint(-a, a) for a in [x, y]]
        assert BLOCK_W % 2 == 0
        w = BLOCK_W/2
        x, y = [int(a/BLOCK_W)*BLOCK_W for a in [x, y]]
        self.setpos(x-OFFSET, y+OFFSET)
        if avoid:
            if avoid.collision(self):
                self.refresh(avoid)


class ScoreBoard(Turtle):

    def __init__(self, screen):
        super().__init__()
        self.setpos(0, int(0.6*screen.canvheight))
        self.color("white")
        self.hideturtle()
        self.score = 0
        self.refresh()

    def refresh(self, txt=None):
        self.clear()
        self.write(txt if txt else f"Score = {self.score}", align='center', font=FONT)

    def increase(self):
        self.score += 1
        self.refresh()
