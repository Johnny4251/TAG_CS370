import socket
import time
import pickle
import threading
from Packet import Packet

class Testing:
    def __init__(self, host='127.0.0.1', port=5555):
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client.connect((host, port))

    def send_data(self, data):
        try:
            self.client.send(data)
        except socket.error as e:
            print(e)

    def unpack_packet(self, data):
        return pickle.loads(data)

    def recv_thread(self):
        # getting response, print response
        while True:
            response = self.client.recv(4096)
            response = self.unpack_packet(response)
            if response.header == "lobby_full":
                print("lobby is full")
                print(f"max lobby count={response.data}")
                self.client.close()
                break
            else:
                print("-----")
                print(f"Header: {response.header}")
                print(f"Data: {response.data}")
                print("-----")

    def run(self):
        threading.Thread(target=self.recv_thread).start()
        print(self.client)
        try:

            for i in range(60):
                # sending packet
                packet = Packet("looping_packet", i)
                data = packet.serialize()
                self.send_data(data)
                time.sleep(1)

            #self.client.close()
            print("DONE SENDING")

        except ConnectionResetError:
            print("host closed connection...")
        except Exception as e:
            print(f"Reached exception:{e}")

if __name__ == "__main__":
    Testing().run()
