import socket
import threading
import pickle
import time
from Packet import Packet
from Handler import PacketHandler
import Utils
from Utils import gen_uniquie_id



# Multithreaded server that can handle multiple clients
class GameServer:
    def __init__(self, host='67.248.194.2', port=3000, client_max=5, debug=False):
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.bind((host, port))
        self.server.listen()
        self.clients_data = {}
        self.clients_conns = {}
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
    def client_thread(self, client_conn, addr,_client_id):
        client_id = _client_id
        while True:
            try:
                # Recv data
                data = client_conn.recv(Utils.BUFFER_SIZE)
                if not data:
                    # WIP
                    print(f"Client {client_id}, sent no data so they are getting removed...")
                    del self.clients_conns[client_id]
                    del self.clients_data[client_id]
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

                packetHandler = PacketHandler(client_conn, self.clients_conns, self.clients_data, client_id, packet)
                packetHandler.handle_event()

            except ConnectionResetError:
                print(f"Client: {client_id}, has closed their connection...")
                del self.clients_conns[client_id]
                del self.clients_data[client_id]
                client_conn.close()
                break

            except Exception as e:
                # this exception is WIP
                print(f"There was an issue with a client: {client_id}, so they are getting removed...")
                print(f"The issue: {e}")
                del self.clients_conns[client_id]
                del self.clients_data[client_id]
                client_conn.close()
                break

    def run(self):
        self.server_startup_banner()

        # main loop
        while True:
            print("listening for new clients...")

            # client accepted -> continue
            client_conn, addr = self.server.accept()
            id = gen_uniquie_id(5)
            print(f"New Client: {id}")
            # Check if lobby is full
            if len(self.clients_conns) < self.client_max:

                for key,client in self.clients_conns.items():
                    response = Packet(source="server", header="server-message", data="Say Hello! A new client has joined!")
                    response = response.serialize()
                    client.send(response)

                self.clients_conns[id] = client_conn
                # Give client a thread
                try:
                    threading.Thread(target=self.client_thread, args=(client_conn, addr,id)).start()
                except Exception as e:
                    print(e)
                
                self.clients_data[id] = [200,200]
                response = Packet(source="server", header="connected", data=id)
                response = response.serialize()
                self.clients_conns[id].send(response)
            else:
                # Full lobby => no thread
                print("rejecting client => lobby full")
                data = Packet(source= "server", header="lobby_full", data=self.client_max)
                data = data.serialize()
                client_conn.send(data)
                client_conn.close()

            print(f"Lobby Size ({len(self.clients_conns)}/{self.client_max})")

if __name__ == "__main__":
    server = GameServer(client_max=5,debug=True)
    server_thread = threading.Thread(target=server.run)
    server_thread.start() 
    server_thread.join() 