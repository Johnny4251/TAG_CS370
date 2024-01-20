import threading
from GameServer import GameServer
import time

class ServerManager:
    def __init__(self):
        pass


if __name__ == "__main__":
    server_one = GameServer(port=12134)
    server_two = GameServer(port=55555)
    threading.Thread(target=server_one.run).start() 
    time.sleep(1)
    threading.Thread(target=server_two.run).start() 

    manager = ServerManager()
