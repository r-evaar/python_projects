from gameObjects import Snake, Food, ScoreBoard, BLOCK_W
from turtle import Screen

w, h = [480, 480]

screen = Screen()
screen.setup(width=w, height=h)
screen.canvwidth = w
screen.canvhight = h
screen.bgcolor("black")
screen.title("Sneaky Snake")

while True:
    try:
        difficulty = screen.textinput("Select Difficulty", "Easy | Medium | Hard").lower()
        assert difficulty in ['easy', 'medium', 'hard']
        break
    except AssertionError:
        continue

snake = Snake(screen, difficulty=difficulty, length=3)
food = Food(screen)
score = ScoreBoard(screen)

while not snake.game_over:
    snake.move_snake()

    if snake.first.distance(food) < BLOCK_W/2:
        food.refresh(avoid=snake)
        score.increase()
        snake.grow()

score.refresh(f"Game Over! - Score = {score.score}")
screen.exitonclick()

