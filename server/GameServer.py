import socket
import threading

# Multithreaded server that can handle multiple clients
class GameServer:
    def __init__(self, host='127.0.0.1', port=5555, client_max=2):
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.bind((host, port))
        self.server.listen()
        self.clients = []
        self.client_max = client_max
    
    def client_thread(self, conn, addr):
        while True:
            try:
                data = conn.recv(4096)
                if not data:
                    print(f"Client {addr} disconnected") # WIP?
                    self.clients.remove(conn)
                    conn.close()
                    break

                print(f"received: {data.decode()} from {addr}")

                for client in self.clients:
                    data = "ack"
                    data = data.encode()
                    client.send(data)

            except Exception as e:
                print(f"An error occurred with client {addr}: {e}")
                self.clients.remove(conn)
                conn.close()
                break

    def run(self):
        print("Server Started...")
        while True:
            conn, addr = self.server.accept()
            print(f"Connected to {addr}")
            if len(self.clients) < self.client_max:
                print("appending new client...")
                self.clients.append(conn)
                threading.Thread(target=self.client_thread, args=(conn, addr)).start()
            else:
                print("rejecting client -> lobby full")
                data = "SERVER REFUSES CONNECTION -> LOBBY FULL"
                conn.send(data.encode())
                conn.close()
            print(f"Lobby Size ({len(self.clients)}/{self.client_max})")

if __name__ == "__main__":
    server = GameServer()
    server.run()