# -*- coding: utf-8 -*-
"""
@author: Sami Safadi
@note: adapted from Michele Vallisneri, https://www.lynda.com/Python-tutorials/Python-Programming-Efficiently
"""

from collections import namedtuple
from math import sin, cos, pi, ceil
import matplotlib; import matplotlib.pyplot as plt; import matplotlib.animation as anim
from IPython.display import display, HTML

Point = namedtuple('Point', 'x y')
degree = pi / 180.0 # conversion between degress and radians

class Turtle(object):
    def __init__(self, terrarium, color='navy'):
        self.pos = Point(0, 0)
        self.angle = 90
        self.pen = True
        self.axes = terrarium.axes
        self.color = color
    
    def forward(self, distance):
        newx = self.pos.x + distance * cos(self.angle * degree)
        newy = self.pos.y + distance * sin(self.angle * degree)       
        if self.pen: 
            line = plt.Line2D((self.pos.x, newx), (self.pos.y, newy), color = self.color)
            self.axes.add_line(line)
        self.pos = Point(newx, newy)
        return self

    def backward(self, distance):
        self.forward(-distance)
        return self

    def left(self, angle):
        self.angle = (self.angle + angle) % 360
        return self

    def right(self, angle):
        self.left(-angle)
        return self

    def pendown(self):
        self.pen = True
        return self

    def penup(self):
        self.pen = False
        return self

    def point(self, width = 2):
        circle = plt.Circle(self.pos, width, color = self.color)
        self.axes.add_patch(circle)
        return self

class Terrarium(object):
    def __init__(self, size=3, animate=False, duration=2):
        # initialize figure
        self.fig = plt.figure(figsize = (size, size))
        self.axes = plt.axes()
        # remove axis ticks and labels
        self.axes.set_xticks([])
        self.axes.set_yticks([])
        # make border transparent
        for side in ['bottom', 'top', 'left', 'right']:
            self.axes.spines[side].set_color('0.9')
        if animate:
            self.axes = AnimatedAxes(self.fig, self.axes, duration)
    
    def rescale(self):
        self.axes.axis('scaled')
        # add some buffer to border so that drawing is not touching the edge
        xmin, xmax, ymin, ymax = self.axes.axis()
        dx = (xmax - xmin) / 50
        self.axes.axis ([xmin-dx, xmax+dx, ymin-dx, ymax+dx])

    # perform when entering and exiting 'with' statement
    def __enter__(self):
        return self
    
    def __exit__(self,*args):
        self.rescale()
        if isinstance(self.axes,AnimatedAxes):
            anim = self.axes.animation()
            display(HTML(anim.to_html5_video()))
            plt.close()

class AnimatedAxes(object):
    def __init__(self, fig, axes, duration=1):
        self.fig = fig
        self.axes = axes
        # grant access to true matplotlib axes to allow Terrarium.rescale()
        self.axis = axes.axis      
        self.duration = duration        
        self.objects = []
    
    def add_line(self,line):
        self.axes.add_line(line)
        self.objects.append(line)
        
    def add_patch(self,patch):
        self.axes.add_patch(patch)
        self.objects.append(patch)
        
    def animate(self,i):
        for obj in self.objects[i*self.dt:(i+1)*self.dt]:
            if isinstance(obj,matplotlib.lines.Line2D):
                self.axes.add_line(obj)
            else:
                self.axes.add_patch(obj)
    
    def animation(self):
        self.dt = max(1,int(len(self.objects) / (self.duration * 30)))
        n = ceil(len(self.objects) / self.dt)        
        rate = self.duration * 1000 / n
        self.axes.clear()
        self.axes.set_xticks([])
        self.axes.set_yticks([])
        for spine in ['bottom','top','left','right']:
            self.axes.spines[spine].set_color('0.9')        
        return matplotlib.animation.FuncAnimation(self.fig,self.animate,blit=False,frames=n,interval=rate,repeat=False)    
  
