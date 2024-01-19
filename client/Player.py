# The player controller or ray caster
import pygame
import numpy as np 
import math as Math
from Ray import Ray
from Vector import Vector

def degreeToRadian(degree):
    return (degree / 180) * Math.pi; 
def radianToDegree(radian):
    return (radian * 180) / Math.pi; 

class Player:
    def __init__(self,pos,ray_increment):
        self.speed = 1
        self.size = 5
        self.col = (255,255,255)
        self.ray_count = 3  # low resolution 
        self.pos = pos
        self.rays = []
        self.divisor = ray_increment # the degree of approximation

    def update_rays(self,theta):
        self.rays = []
        for i in np.arange(0,self.ray_count,self.divisor):
            degree = radianToDegree(theta) + 4 * i
            self.rays.append( Ray(self.pos,degreeToRadian(degree)))

    def update(self,x,y):
        self.pos.x = x
        self.pos.y = y
    
    def look(self,window,walls,objs):
        for ray in self.rays:
            pt = None
            closest = None
            record = 9999 # INFINITY.....
            col = None
            circ = None
            for wall in walls:
                pt = ray.cast(wall)
                if(pt):
                    dist = Vector.dist(self.pos,pt)
                    if(dist < record):
                        record = dist
                        closest = pt
                        col = wall.col
            for obj in objs:
                pt = ray.cast_circle(obj)
                if(pt):
                    dist = Vector.dist(self.pos,pt[0])
                    if(dist < record):
                        record = dist
                        closest = pt[0]
                        circ = pt[1]
                        col = obj.col

            if (closest):
                #Draw Ray
                pygame.draw.line(window,(255,243,0,1),(self.pos.x,self.pos.y),(closest.x,closest.y))
                pygame.draw.circle(window,col,(closest.x,closest.y),1)
                if(circ != None):
                    pygame.draw.circle(window,col,(circ.x,circ.y),1)
 
    def render(self,window):
        pygame.draw.circle(window,self.col,(self.pos.x,self.pos.y),self.size)