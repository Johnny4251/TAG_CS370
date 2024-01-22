import socket
from Packet import Packet

class PacketHandler:
    def __init__(self, conn, clients, packet):
        self.conn = conn
        self.clients = clients
        self.packet = packet


    def handle_event(self):
        if self.packet.header == "p_req_tag":
            self.__p_req_tag_event()
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
            self.clients[data] = self.conn
            print(f"client joining with tag: {data}")
            data = Packet(source="server", dest=self.packet.data, header="tag_accepted", data=self.packet.data)
            data = data.serialize()
            self.conn.send(data)
        else:
            # tag is taken
            print("client requested a tag that is already in use, kicking...")
            data = Packet(source="server", dest=self.packet.data, header="p_tag_taken", data=self.packet.data)
            data = data.serialize()
            self.conn.send(data)
            self.conn.close()
