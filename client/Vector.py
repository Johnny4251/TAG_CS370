# 2 dimensional vector representation
import math as Math
class Vector:
    def __init__(self,x=None,y=None):
        self.x = x
        self.y = y

    def fromAngle(angle,v):
        if(v == None):
            v = Vector()
        v.x = Math.cos(angle)
        v.y = Math.sin(angle)
        return v

    def dist(v1,v2):
        dx = v1.x - v2.x
        dy = v1.y - v2.y
        return Math.sqrt(dx * dx + dy * dy)

    def mag(self):
        x = self.x
        y = self.y
        return Math.sqrt(x * x + y * y)
    
    def div(self,v):
        if(type(v) == int or type(v) == float):
            self.x /= v
            self.y /= v
        else:
            self.x /= v.x
            self.y /= v.y

    def add(self,v):
        if(type(v) == int or type(v) == float):
            self.x += v
            self.y += v
        else:
            self.x += v.x
            self.y += v.y

    def sub(self,v):
        if(type(v) == int or type(v) == float):
            self.x -= v
            self.y -= v
        else:
            self.x -= v.x
            self.y -= v.y
    
    def mul(self,v):
        if(type(v) == int or type(v) == float):
            self.x *= v
            self.y *= v
        else:
            self.x *= v.x
            self.y *= v.y

    def normalize(self):
        m = self.mag()
        if(m>0):
            self.div(m)

    def scale(self,m):
        m = self.mag()
        if(m>0):
            self.mul(m)
    





        

           
    

  

