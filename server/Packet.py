import pickle

class Packet:
    def __init__(self, header, data=""):
        self.header = header
        self.data = data

    def serialize(self):
        return pickle.dumps(self)