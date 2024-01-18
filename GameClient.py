import pygame
import socket

class Player:
    def __init__(self, nametag):
        self.nametag = nametag

class GameClient:
    def __init__(self, host='127.0.0.1', port=5555):
        # implement socket logic here later
        pass
    
    def send_data(data):
        pass

    def run(self):
        pygame.init()
        screen = pygame.display.set_mode((800, 600))

        clock = pygame.time.Clock()

        # main loop
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

            keys = pygame.key.get_pressed()
            print(keys)
            
            screen.fill((0, 0, 0))

            pygame.display.flip()
            clock.tick(60) # 60fps cap

        pygame.quit()

if __name__ == "__main__":
    GameClient.run()