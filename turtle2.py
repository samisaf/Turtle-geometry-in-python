# -*- coding: utf-8 -*-
"""
@author: Sami Safadi
@note: a different implementation of the turtle 
"""

from collections import namedtuple
from math import sin, cos, pi
import matplotlib.pyplot as plt

rad2deg = pi / 180.0 # conversion between degress and radians
T = namedtuple('Turtle', 'color angle x y')

def Turtle(color='navy', angle=0, x=0, y=0):
    return T(color, [angle], [x], [y])

def forward(distance):
    def move(turtle):
        newx = turtle.x[-1] + distance * cos(turtle.angle[-1] * rad2deg)
        newy = turtle.y[-1] + distance * sin(turtle.angle[-1] * rad2deg)
        turtle.x.append(newx)
        turtle.y.append(newy)
        return turtle
    return move

def back(distance):
    return forward(-distance)

def left(angle):
    def turn(turtle):
        newangle = (turtle.angle[-1] + angle) % 360
        turtle.angle.append(newangle)
        return turtle
    return turn

def right(angle):
    return left(-angle)

def plot(turtle, size=5):
    xmin, xmax = min(turtle.x), max(turtle.x)
    ymin, ymax = min(turtle.y), max(turtle.y)
    BUFFER = (xmax - xmin) / 50   
    plt.figure(figsize = (size, size))
    plt.axes().axis('scaled')
    plt.xlim(xmin - BUFFER, xmax + BUFFER)
    plt.ylim(ymin - BUFFER, ymax + BUFFER)
    plt.plot(turtle.x, turtle.y, color=turtle.color)
    plt.show()

def test1():
    t1 = Turtle()
    for _ in range(36):
        left(10)(t1)
        for __ in range(4):
            forward(10)(t1)
            left(90)(t1)
    plot(t1)

def test2():
    t = Turtle(angle=90)
    pattern = [forward(100),right(90),forward(100),right(90),forward(50),
                right(90),forward(50),right(90),forward(100),right(90),
                forward(25),right(90),forward(25),right(90),forward(50)]
    for _ in range(9):
        [p(t) for p in pattern]
        right(50)(t)
        forward(50)(t)
    plot(t)

if __name__ == '__main__':
    test1()
    test2()