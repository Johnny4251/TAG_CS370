# A simple way to represent walls or boundaries
import pygame
from Vector import Vector

class Boundary:
    def __init__(self,aVec,bVec,inpCol=(255,255,255)):
        self.a = aVec
        self.b = bVec
        self.col = inpCol
    
    def render(self,window):
        pygame.draw.line(window,self.col,(self.a.x,self.a.y),(self.b.x,self.b.y))

