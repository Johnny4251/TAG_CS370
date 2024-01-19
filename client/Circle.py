# Our representation of a circle
import pygame
from Vector import Vector
class Circle:
    def __init__(self,x,y,d,col=(255,255,255)):
        self.pos = Vector(x,y)
        self.diameter = d
        self.radius = d/2
        self.col = col
    
    def render(self,window):
        pygame.draw.circle(window,self.col,(self.pos.x,self.pos.y),self.radius)

