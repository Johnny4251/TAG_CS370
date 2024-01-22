import pygame
import math as Math
import random
from Vector import Vector
from Player import Player

class GameClient:
    def __init__(self,client_socket=None):
        pygame.init()
        print("HELLO")
        self.debug_mode = False
        self.window_should_stay_open = True
        self.window_width = 800
        self.window_height = 600
        self.window = pygame.display.set_mode((self.window_width, self.window_height))
        self.keys = []
        self.walls = []
        self.circles = []
        self.player = Player(Vector(200,200),0.1)
        self.clock = pygame.time.Clock()
        self.mouseX = 0
        self.mouseY = 0
        self.mosueB = -1
        #these can be removed purely for demo scene
        self.amp = 50
        self.freq = 20
        self.offy = 200
        return
    
    def poll_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                    self.window_should_stay_open = False
        self.keys = pygame.key.get_pressed()
        self.mouseX,self.mouseY = pygame.mouse.get_pos()
        self.mosueB = pygame.mouse.get_pressed()
        return

    def handle_keys(self):
        if(self.keys[pygame.K_ESCAPE]):
            self.window_should_stay_open = False
        if self.keys[pygame.K_p]:
                self.debug_mode =  not self.debug_mode
        past_state = (self.player.pos.x,self.player.pos.y)
        if self.keys[pygame.K_w]:
                self.player.update(self.player.pos.x,  self.player.pos.y - self.player.speed)
        if self.keys[pygame.K_s]:
                self.player.update(self.player.pos.x,  self.player.pos.y + self.player.speed)
        if self.keys[pygame.K_a]:
                self.player.update(self.player.pos.x - self.player.speed,self.player.pos.y)
        if self.keys[pygame.K_d]:
                self.player.update(self.player.pos.x + self.player.speed,self.player.pos.y)
        self.player.check_collisions(self.walls)
    
             
             
        return

    def update(self):
        self.poll_events()
        self.handle_keys()
        dx = self.mouseX - (self.player.pos.x)
        dy = self.mouseY - (self.player.pos.y)
        theta = Math.atan2(dy,dx)
        self.player.update_rays(theta)

        # This is for the default scene and can be deleted later
        if(len(self.circles) > 1):
            self.circles[1].pos.x = (self.circles[1].pos.x + 1) % self.window_width 
            self.circles[1].pos.y = Math.sin(self.circles[1].pos.x/self.freq) * self.amp + self.offy
            if(self.circles[1].pos.x == 0):
                 self.amp = random.randint(10,200)
                 self.freq = random.randint(10,200)
                 self.offy = random.randint(0,self.window_height-30)    
    
        self.clock.tick(60) # fixed 60 tick update 
        return
    
    def render(self):
        self.window.fill((0, 0, 0))
        if(self.debug_mode):
            for x in self.walls:
                x.render(self.window)
            if(len(self.circles) > 1):
                 for c in self.circles:
                    c.render(self.window)
                 
        if(self.mosueB[0]):
             self.player.look(self.window,self.walls,self.circles)
        self.player.render(self.window)
        pygame.display.flip()
        return
    
    def kill_window(self):
        pygame.quit()
        return