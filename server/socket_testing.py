import socket
import time
import pickle
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

    def run(self):
        print(self.client)
        try:

            for i in range(60):
                # sending packet
                packet = Packet("looping_packet", i)
                data = packet.serialize()
                self.send_data(data)

                # getting response, print response
                response = self.client.recv(4096)
                response = self.unpack_packet(response)
                if response.header == "lobby_full":
                    print("lobby is full")
                    print(f"max lobby count={response.data}")
                else:
                    print("-----")
                    print(f"Header: {response.header}")
                    print(f"Data: {response.data}")
                    print("-----")
                    time.sleep(1)

            #self.client.close()
            print("DONE")
        except ConnectionResetError:
            print("host closed connection...")
        except Exception as e:
            print(f"Reached exception:{e}")

if __name__ == "__main__":
    Testing().run()
