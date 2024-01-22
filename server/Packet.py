import pickle

# Packet for communication
class Packet:
    def __init__(self, source, header, dest="broadcast", data=""):
        self.source = source
        self.dest = dest
        self.header = header
        self.data = data

    def serialize(self):
        return pickle.dumps(self)