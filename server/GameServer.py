import socket
import threading
import pickle
from Packet import Packet

# Multithreaded server that can handle multiple clients
class GameServer:
    def __init__(self, host='127.0.0.1', port=5555, client_max=2):
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.bind((host, port))
        self.server.listen()
        self.clients = []
        self.client_max = client_max
    
    def unpack_packet(self, data):
        return pickle.loads(data)

    def client_thread(self, conn, addr):
        while True:
            try:
                data = conn.recv(4096)
                if not data:
                    # WIP
                    print(f"Client {addr}, sent no data so they are getting removed...")
                    self.clients.remove(conn)
                    conn.close()
                    break

                #print(f"received: {data} from {addr}")
                packet = self.unpack_packet(data)
                print(f"----{addr}----")
                print(f"Header: \t{packet.header}")
                print(f"Data  : \t{packet.data}")
                print(f"----------------------------")

                for client in self.clients:
                    response = Packet(header="server", data="data from "+str(addr)+" ack")
                    response = response.serialize()
                    client.send(response)

            except ConnectionResetError:
                print(f"Client: {addr}, has closed their connection...")
                self.clients.remove(conn)
                conn.close()
                break

            except Exception as e:
                # this exception is WIP
                print(f"There was an issue with a client: {addr}, so they are getting removed...")
                print(f"The issue: {e}")
                self.clients.remove(conn)
                conn.close()
                break

    def run(self):
        print("Server Started...")
        while True:
            conn, addr = self.server.accept()
            print(f"New Client: {addr}")
            if len(self.clients) < self.client_max:
                print("appending new client...")
                self.clients.append(conn)

                for client in self.clients:
                    response = Packet(header="server", data="Say Hello! A new client has joined!")
                    response = response.serialize()
                    client.send(response)

                threading.Thread(target=self.client_thread, args=(conn, addr)).start()
            else:
                print("rejecting client => lobby full")
                data = Packet(header="lobby_full", data=self.client_max)
                data = data.serialize()
                conn.send(data)
                conn.close()

            print(f"Lobby Size ({len(self.clients)}/{self.client_max})")

if __name__ == "__main__":
    server = GameServer(client_max=5)
    server.run()