import socket
import time
import pickle
import threading
from Packet import Packet

class Testing:
    def __init__(self, host='127.0.0.1', port=5555, listening=True):
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client.connect((host, port))
        self.listening = listening

        response = self.client.recv(4096)
        response = self.unpack_packet(response)
        if response.header == "lobby_full":
            print("lobby is full")
            print(f"max lobby count={response.data}")
            self.client.close()
            self.listening = False
            exit()
        self.name = input("what is your name? ")


    def send_data(self, data):
        try:
            self.client.send(data)
        except socket.error as e:
            print(e)

    def unpack_packet(self, data):
        return pickle.loads(data)

    def recv_thread(self):
        # getting response, print response
        while self.listening:
            response = self.client.recv(4096)
            response = self.unpack_packet(response)
            if response.header == "lobby_full":
                print("lobby is full")
                print(f"max lobby count={response.data}")
                self.client.close()
                self.listening = False
                exit()
            elif response.header == "p_tag_taken":
                print("That tag is already taken, please try again with a new tag!")
                self.client.close()
                exit(0)
            else:
                print("-----")
                print(f"From: {response.source}")
                print(f"Header: {response.header}")
                print(f"Data: {response.data}")
                print("-----")

    def run(self):
        threading.Thread(target=self.recv_thread).start()
        print(self.client)

        try:
            text = input("Choose a tag: ")

            print("client simulation running...")
            time.sleep(1)
            text = input("Choose a tag: ")

            packet = Packet(self.name, "p_req_tag", text)
            packet = packet.serialize()
            self.send_data(packet)

            while True:
                time.sleep(1)
                text = input("Pick a msg: ")
                if text == "exit()": break

                packet = Packet(self.name, "msg", text)
                packet = packet.serialize()
                self.send_data(packet)
                
            self.client.close()

        except ConnectionResetError:
            print("host closed connection...")
        except Exception as e:
            print(f"Reached exception:{e}")

if __name__ == "__main__":
    Testing().run()
