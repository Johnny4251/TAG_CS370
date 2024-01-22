import threading
from GameServer import GameServer
import time

class ServerManager:
    def __init__(self):
        pass


if __name__ == "__main__":
    client_max = input("Max number of clients: ")
    addr = input("IP? ")
    port = input("Port? ")
    debug_input = input("Debug mode?(y or n) ")
    debug = False

    if debug_input[0] == 'y':
        debug = True
    
    server = GameServer(host=addr, port=int(port), client_max=client_max, debug=debug)
    server.run()