import pygame
import math as Math
import random
from Vector import Vector
from Circle import Circle
from Player import Player

class GameClient:
    def __init__(self,client_socket=None):     
        pygame.init()
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
        self.client_socket = client_socket
        self.client_socket.start_thread()
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
        key_hit = None
        # Could turn into a buffer of inputs that then gets sent and processed on server
        if self.keys[pygame.K_w]:
                key_hit = pygame.K_w
                self.player.update(self.player.pos.x,  self.player.pos.y - self.player.speed)
        elif self.keys[pygame.K_s]:
                key_hit = pygame.K_s
                self.player.update(self.player.pos.x,  self.player.pos.y + self.player.speed)
        elif self.keys[pygame.K_a]:
                key_hit = pygame.K_a
                self.player.update(self.player.pos.x - self.player.speed,self.player.pos.y)
        elif self.keys[pygame.K_d]:
                key_hit = pygame.K_d
                self.player.update(self.player.pos.x + self.player.speed,self.player.pos.y)
        result = self.player.check_collisions(self.walls)  
        if(not result and key_hit != None):
             self.client_socket.send_data("key-press",key_hit)
                  
        return

    def update(self):
        self.poll_events()
        self.handle_keys()
        dx = self.mouseX - (self.player.pos.x)
        dy = self.mouseY - (self.player.pos.y)
        theta = Math.atan2(dy,dx)
        self.player.update_rays(theta)    
        self.clock.tick(60) # fixed 60 tick update 
        return
    
    def render(self):
        self.window.fill((0, 0, 0))
        if(self.debug_mode):
            for x in self.walls:
                x.render(self.window)
            if(self.client_socket.player_data != None):
                 for k,c in self.client_socket.player_data.items():
                    p = Circle(c[0],c[1],10)
                    p.render(self.window)
                 
        if(self.mosueB[0]):
             self.player.look(self.window,self.walls,self.client_socket.player_data,self.client_socket.id)
        self.player.render(self.window)
        pygame.display.flip()
        return
    
    def kill_window(self):
        pygame.quit()
        self.client_socket.send_data("kill-socket")
        return