import turtle

# Set up Turtle
turtle.speed(0)  # Set speed to the fastest
turtle.hideturtle()  # Hide the turtle cursor
turtle.bgcolor('white')  # Set background color to white

# Draw cell membrane
turtle.penup()
turtle.goto(-200, -200)
turtle.pendown()
turtle.pensize(3)
turtle.color('black')
turtle.circle(200)

# Draw nucleus
turtle.penup()
turtle.goto(-100, -100)
turtle.pendown()
turtle.color('lightblue')
turtle.begin_fill()
turtle.circle(100)
turtle.end_fill()

# Draw nucleolus
turtle.penup()
turtle.goto(-70, -70)
turtle.pendown()
turtle.color('darkblue')
turtle.begin_fill()
turtle.circle(30)
turtle.end_fill()

# Draw cytoplasm
turtle.penup()
turtle.goto(0, 0)
turtle.pendown()
turtle.color('lightgreen')
turtle.begin_fill()
turtle.circle(200)
turtle.end_fill()

# Draw mitochondria
turtle.penup()
turtle.goto(100, 0)
turtle.pendown()
turtle.color('red')
turtle.begin_fill()
turtle.circle(50)
turtle.end_fill()

# Draw endoplasmic reticulum
turtle.penup()
turtle.goto(0, 100)
turtle.pendown()
turtle.color('purple')
turtle.pensize(1)
turtle.forward(50)
turtle.right(90)
turtle.forward(50)
turtle.left(90)
turtle.forward(50)
turtle.right(90)
turtle.forward(50)
turtle.left(90)
turtle.forward(50)

# Keep the drawing window open until closed by the user
turtle.done()