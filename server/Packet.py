import pickle

# Packet for communication
class Packet:
    def __init__(self, source, header, data=""):
        self.header = header
        self.data = data

    def serialize(self):
        return pickle.dumps(self)