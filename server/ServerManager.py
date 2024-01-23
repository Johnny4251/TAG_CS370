import threading
from GameServer import GameServer
import time

if __name__ == "__main__":
    server = GameServer(debug=False)
    server_thread = threading.Thread(target=server.run)
    server_thread.start()

    time.sleep(1) # give thread a sec to catch up
    cmd = ""
    while cmd != "kill":
        cmd = input("@TagServer>> ")
        if cmd == "list clients":
            print(server.clients_conns)
        elif cmd == "/help":
            print("===COMMANDS===")
            print(">> list clients")
            print(">> /help")
            print("==============")
        else:
            print("Command not found! Use /help")

    server.kill()
    server_thread.join()