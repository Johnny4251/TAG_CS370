import socket
import pickle
from Packet import Packet

class ClientSocket:
    def __init__(self, host='127.0.0.1', port=3000, listening=True):

        self.socket_client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket_client.connect((host, port))
        self.socket_client_listening = listening

        response = self.socket_client.recv(4096)
        response = self.unpack_packet(response)
        if response.header == "lobby_full":
            print("lobby is full")
            print(f"max lobby count={response.data}")
            self.client.close()
            self.listening = False
            return None
        return 
    
    def unpack_packet(self, data):
        return pickle.loads(data)