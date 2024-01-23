# Map builder located at https://editor.p5js.org/Blungus23/full/j1zqoJMKq
import json
import threading
from ClientSocket import ClientSocket
from Vector import Vector
from GameClient import GameClient 
from Boundary import Boundary
from Circle import Circle

def gen_def_scene(client):
     wall = Boundary(Vector(375, 250), Vector(375,50),(255,0,0))
     client.walls.append(wall)
     wall = Boundary(Vector(100, 100), Vector(250, 250))
     client.walls.append(wall)
     wall = Boundary( Vector(50, 100), Vector(250, 100))
     client.walls.append(wall)
     wall = Boundary(Vector(50, 50), Vector(250, 50))
     client.walls.append(wall)

     wall = Boundary(Vector(0, 0), Vector(client.window_width, 0),(0,0,0))
     client.walls.append(wall)   
     wall = Boundary(Vector(client.window_width, 0), Vector(client.window_width, client.window_height),(0,0,0))
     client.walls.append(wall)   
     wall = Boundary(Vector(client.window_width, client.window_height), Vector(0, client.window_height),(0,0,0))
     client.walls.append(wall) 
     wall = Boundary(Vector(0, client.window_height), Vector(0, 0),(0,0,0))
     client.walls.append(wall)    

     client.circles.append(Circle(300,200,25,(255,0,255)))
     client.circles.append(Circle(0,200,12,(0,255,255)))
     return

def gen_scene_from_file(client,file_name):
    f = open(file_name)
    data = json.load(f)
    for obj in data:
        for bound in obj:
            a = (bound['a']['x'],bound['a']['y'])
            b = (bound['b']['x'],bound['b']['y'])
            col = (bound['col']['r'],bound['col']['g'],bound['col']['b'])
            wall = Boundary(Vector(a), Vector(b),col)
            client.walls.append(wall)    
    f.close()
    # Generate border wall regardless of map data
    wall = Boundary(Vector(0, 0), Vector(client.window_width, 0),(0,0,0))
    client.walls.append(wall)   
    wall = Boundary(Vector(client.window_width, 0), Vector(client.window_width, client.window_height),(0,0,0))
    client.walls.append(wall)   
    wall = Boundary(Vector(client.window_width, client.window_height), Vector(0, client.window_height),(0,0,0))
    client.walls.append(wall) 
    wall = Boundary(Vector(0, client.window_height), Vector(0, 0),(0,0,0))
    client.walls.append(wall)   
    return

if __name__ == "__main__":
    gameSocket = ClientSocket('127.0.0.1')
    gameClient = GameClient(gameSocket)
    #gen_def_scene(gameClient)
    gen_scene_from_file(gameClient,'map_data2.json')
    while gameClient.window_should_stay_open:
        gameClient.update()
        gameClient.render()
    gameClient.kill_window()