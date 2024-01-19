# Simple Ray Caster
import math as Math
from Vector import Vector

def length(x,y):
        return Math.sqrt((x*x) + (y*y))

# this number represents how close a player has to be in order to see 
# a different player with their flashlight
CAST_SEARCH_LIMIT = 250
class Ray:
    def __init__(self, pos, angle):
        self.pos = pos
        self.dir = Vector.fromAngle(angle,None)

    def cast(self,boundary):
        x1 = boundary.a.x
        y1 = boundary.a.y
        x2 = boundary.b.x
        y2 = boundary.b.y
        
        x3 = self.pos.x
        y3 = self.pos.y
        x4 = self.pos.x + self.dir.x
        y4 = self.pos.y + self.dir.y

        den = (x1 - x2) * (y3 - y4) - (y1 - y2) * (x3 - x4)

        #if denominator is zero then the ray and boundary are parallel
        if (den == 0): return

        t = ((x1 - x3) * (y3 - y4) - (y1 - y3) * (x3 - x4)) / den
        u = -((x1 -x2) * (y1 - y3) - (y1 - y2) * (x1 - x3)) / den

        if (t > 0 and t < 1 and u > 0):
            pt = Vector()
            pt.x = x1 + t * (x2 - x1)
            pt.y = y1 + t * (y2 - y1)
            return pt
        return
    
    def signedDstToCircle(self,px,py,cx,cy,cd):
        radius = cd/2
        return length(cx-px,cy-py) - radius

    def cast_circle(self,circle):
         x1 = self.pos.x
         y1 = self.pos.y
         x2 = self.pos.x + self.dir.x
         y2 = self.pos.y + self.dir.y
         dx = x2 - x1
         dy = y2 - y1

         px = x1
         py = y1

         for i in range(0,CAST_SEARCH_LIMIT,1):
             d = self.signedDstToCircle(px,py,circle.pos.x,circle.pos.y,circle.diameter)
             if(d <= 0):
                 pt1 = Vector(px,py)
                 pt2 = self.reverse_cast_circle(px,py,circle)
                 return [pt1,pt2]
             px += dx
             py += dy
         return  
    def reverse_cast_circle(self,px,py,circle):
             x1 = self.pos.x
             y1 = self.pos.y
             x2 = self.pos.x + self.dir.x
             y2 = self.pos.y + self.dir.y
             dx = x2 - x1
             dy = y2 - y1
             for i in range(0,CAST_SEARCH_LIMIT,1):
                    d = self.signedDstToCircle(px,py,circle.pos.x,circle.pos.y,circle.diameter)
                    if(d >= 0):
                        pt1 = Vector(px,py)
                        return pt1
                    px += dx
                    py += dy
             return    
        
               