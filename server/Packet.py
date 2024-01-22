import pickle

# Packet for communication
class Packet:
    def __init__(self, source, header, dest="", data=""):
        self.source = source
        self.header = header
        self.data = data

    def serialize(self):
        return pickle.dumps(self)