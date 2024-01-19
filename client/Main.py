from Vector import Vector
from GameClient import GameClient 
from Boundary import Boundary
from Circle import Circle

def generateScene(client):
     wall = Boundary(Vector(375, 250), Vector(375,50),(255,0,0))
     client.walls.append(wall)
     wall = Boundary(Vector(100, 100), Vector(250, 250))
     client.walls.append(wall)
     wall = Boundary( Vector(50, 100), Vector(250, 100))
     client.walls.append(wall)
     wall = Boundary(Vector(50, 50), Vector(250, 50))
     client.walls.append(wall)
     client.circles.append(Circle(300,200,25,(255,0,255)))
     client.circles.append(Circle(0,200,12,(0,255,255)))
     return
     
if __name__ == "__main__":
    gameClient = GameClient()
    generateScene(gameClient)
    while gameClient.window_should_stay_open:
        gameClient.update()
        gameClient.render()
    gameClient.kill_window()