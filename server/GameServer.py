import socket
import threading
import pickle
import time
from Packet import Packet
from Handler import PacketHandler

# Multithreaded server that can handle multiple clients
class GameServer:
    def __init__(self, host='127.0.0.1', port=3000, client_max=5, debug=False):
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.bind((host, port))
        self.server.listen()
        
        self.clients = []
        self.clients_dict = {}
        self.client_max = client_max
        self.debug = debug
    
    def server_startup_banner(self):
        banner_lines = [
            "+-------------------------------------+",
            "|       Python Tag Game Server        |",
            "|          Starting Up...             |",
            "+-------------------------------------+"
        ]
        for line in banner_lines:
            print(line)

    # Used to deserialize Packets
    def unpack_packet(self, data):
        return pickle.loads(data)

    # Thread created to handle each client
    def client_thread(self, client_conn, addr):
        while True:
            try:
                # Recv data
                data = client_conn.recv(4096)
                if not data:
                    # WIP
                    print(f"Client {addr}, sent no data so they are getting removed...")
                    self.clients.remove(client_conn)
                    client_conn.close()
                    break

                # Deserialize data into packet
                packet = self.unpack_packet(data)
                if self.debug:
                    print(f"----{addr}----")
                    print(f"Source: \t{packet.source}")
                    print(f"Header: \t{packet.header}")
                    print(f"Data  : \t{packet.data}")
                    print(f"----------------------------")

                handler = PacketHandler(client_conn, self.clients, packet)
                handler.handle_event()

                for client in self.clients:
                    if packet.header == "msg":
                        response = Packet(source=packet.source, header="Message", data=packet.data)
                        response = response.serialize()
                        client.send(response)
                    else:
                        response = Packet(source="server", header="header", data=packet.data)
                        response = response.serialize()
                        client.send(response)

            except ConnectionResetError:
                print(f"Client: {addr}, has closed their connection...")
                self.clients.remove(client_conn)
                client_conn.close()
                break

            except Exception as e:
                # this exception is WIP
                print(f"There was an issue with a client: {addr}, so they are getting removed...")
                print(f"The issue: {e}")
                self.clients.remove(client_conn)
                client_conn.close()
                break

    def run(self):
        self.server_startup_banner()

        # main loop
        while True:
            print("listening for new clients...")

            # client accepted -> continue
            client_conn, addr = self.server.accept()
            print(f"New Client: {addr}")

            # Check if lobby is full
            if len(self.clients) < self.client_max:
                #self.clients.append(client_conn)

                for client in self.clients:
                    response = Packet(source="server", header="header", data="Say Hello! A new client has joined!")
                    response = response.serialize()
                    client.send(response)

                # Give client a thread
                try:
                    threading.Thread(target=self.client_thread, args=(client_conn, addr)).start()
                except Exception as e:
                    print(e)
            else:
                # Full lobby => no thread
                print("rejecting client => lobby full")
                data = Packet(source= "server", header="lobby_full", data=self.client_max)
                data = data.serialize()
                client_conn.send(data)
                client_conn.close()

            print(f"Lobby Size ({len(self.clients)}/{self.client_max})")

if __name__ == "__main__":
    server = GameServer(client_max=5)
    server_thread = threading.Thread(target=server.run)
    server_thread.start() 
    server_thread.join() 