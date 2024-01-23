import socket
from Packet import Packet
import Utils

class PacketHandler:
    def __init__(self, client_conn, clients_conns, clients_data, client_id, packet):
        self.client_conn = client_conn
        self.clients_conns = clients_conns
        self.clients_data = clients_data
        self.client_id = client_id
        self.packet = packet


    def handle_event(self):
        if self.packet.header == "p_req_tag":
            self.__p_req_tag_event()
        elif self.packet.header == "key-press":
            self.__key_press_event()
        elif self.packet.header == "kill-socket":
            self.__kill_socket_event()
        elif self.packet.header == "p_flashlight_on":
            pass
        elif self.packet.header == "p_flashlight_off":
            pass
        elif self.packet.header == "p_is_it":
            pass

    def __kill_socket_event(self):
        print("DISCONNECT: ",end="")
        print(self.packet.source)
        response = Packet(source=self.packet.source, header="kill-socket", data=self.packet.data)
        response = response.serialize()
        self.client_conn.send(response)

    def __key_press_event(self):
        print("key_press_event")
        if(self.packet.data == 119):
            self.clients_data[self.client_id][1] -= Utils.HIDER_SPEED
        elif(self.packet.data == 115):
            self.clients_data[self.client_id][1] += Utils.HIDER_SPEED
        elif(self.packet.data == 97):
            self.clients_data[self.client_id][0] -= Utils.HIDER_SPEED
        elif(self.packet.data == 100):
            self.clients_data[self.client_id][0] += Utils.HIDER_SPEED
        for key,client in self.clients_conns.items():
            response = Packet(source="server", header="player-update", data=self.clients_data)
            response = response.serialize()
            client.send(response)

    # deprecated, will be removed
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
