import turtle
import colorsys
import random

# Setup screen
screen = turtle.Screen()
screen.bgcolor("black")
t = turtle.Turtle()
t.speed(0)
t.width(2)

# Function to draw the heart shape
def draw_heart():
    t.begin_fill()
    t.left(140)
    t.forward(111.65)
    for _ in range(200):
        t.right(1)
        t.forward(1)
    t.left(120)
    for _ in range(200):
        t.right(1)
        t.forward(1)
    t.forward(111.65)
    t.end_fill()
    t.hideturtle()

# Function to create a gradient color palette
def gradient_fill(t, steps=30):
    for i in range(steps):
        hue = i / steps
        r, g, b = colorsys.hsv_to_rgb(hue, 0.8, 0.9)
        t.color((r, g, b), (r, g, b))
        t.begin_fill()
        t.circle(150 - i * 4)
        t.end_fill()

# Add twinkling stars
def draw_stars(num=50):
    star = turtle.Turtle()
    star.hideturtle()
    star.speed(0)
    star.color("white")
    star.penup()
    for _ in range(num):
        x = random.randint(-300, 300)
        y = random.randint(-300, 300)
        star.goto(x, y)
        star.dot(random.randint(2, 5))

# Write message inside the heart
def write_message():
    t.penup()
    t.goto(0, 20)
    t.color("white")
    t.hideturtle()
    t.write("LOVED", align="center", font=("Arial", 20, "bold"))

# Main drawing
turtle.colormode(1.0)  # Use 0–1 RGB values
draw_stars()
t.penup()
t.goto(0, -100)
t.pendown()
t.color("red", "hotpink")
draw_heart()
write_message()

turtle.done()