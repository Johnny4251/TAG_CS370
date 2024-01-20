import json
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

     wall = Boundary(Vector(0, 0), Vector(client.window_width, 0))
     client.walls.append(wall)   
     wall = Boundary(Vector(client.window_width, 0), Vector(client.window_width, client.window_height))
     client.walls.append(wall)   
     wall = Boundary(Vector(client.window_width, client.window_height), Vector(0, client.window_height))
     client.walls.append(wall) 
     wall = Boundary(Vector(0, client.window_height), Vector(0, 0))
     client.walls.append(wall)   

     client.circles.append(Circle(300,200,25,(255,0,255)))
     client.circles.append(Circle(0,200,12,(0,255,255)))
     return

def gen_scene_from_file(client,file_name):
    f = open(file_name)
    data = json.load(f)
    for bound in data[0]:
        ax = bound['a']['x']
        ay = bound['a']['y']
        bx = bound['b']['x']
        by = bound['b']['y']
        r = bound['col']['r']
        g = bound['col']['g']
        b = bound['col']['b']
        wall = Boundary(Vector(ax, ay), Vector(bx, by),(r,g,b))
        client.walls.append(wall)    
    f.close()
    pass
     
if __name__ == "__main__":
    gameClient = GameClient()
    #gen_def_scene(gameClient)
    gen_scene_from_file(gameClient,'map_data.json')
    while gameClient.window_should_stay_open:
        gameClient.update()
        gameClient.render()
    gameClient.kill_window()