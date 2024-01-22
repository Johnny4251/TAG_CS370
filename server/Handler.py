import socket
from Packet import Packet

class PacketHandler:
    def __init__(self, conn, clients, packet):
        self.conn = conn
        self.clients = clients
        self.packet = packet
    

    def handle_event(self):
        if self.packet.header == "p_req_tag":
            pass
        elif self.packet.header == "p_key_press":
            pass
        elif self.packet.header == "p_direction":
            pass
        elif self.packet.header == "p_flashlight_on":
            pass
        elif self.packet.header == "p_flashlight_off":
            pass
        elif self.packet.header == "p_is_it":
            pass

    def __p_req_tag_event(self):
        data = self.packet.data
        if data not in self.clients:
            
            pass
        else:
            # tag is taken
            print("client requested a key that is already in use, rejecting")
            data = Packet(source="server", dest=self.packet.data, header="key_taken", data=self.packet.data)
            data = data.serialize()
            self.conn.send(data)
            self.conn.close()
            