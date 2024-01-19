import socket
import time

class Testing:
    def __init__(self, host='127.0.0.1', port=5555):
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client.connect((host, port))

    def send_data(self, data):
        try:
            self.client.send(data.encode())
        except socket.error as e:
            print(e)

    def run(self):
        for i in range(50):
            self.send_data("testing #" + str(i))
            print("sent data ", i)
            recv_data = self.client.recv(4096)
            print("RECV: " + recv_data.decode())
            time.sleep(1)
        print("DONE")
        self.client.close()

if __name__ == "__main__":
    Testing().run()
