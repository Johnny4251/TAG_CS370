import threading
from GameServer import GameServer
import time

COMMANDS = ["kill", "list clients", "/help"]

if __name__ == "__main__":
    server = GameServer(debug=False)
    server_thread = threading.Thread(target=server.run)
    server_thread.start()

    time.sleep(1) # give thread a sec to catch up
    cmd = ""
    while cmd != COMMANDS[0]: # kill
        cmd = input("@TagServer>> ")
        if cmd == COMMANDS[1]: # list clients
            print(server.clients_conns)
        elif cmd == COMMANDS[2]: # /help
            print("===COMMANDS===")
            for command in COMMANDS:
                print(">> " + command)
            print("==============")
        else:
            print("Command not found! Use /help")

    server.kill()
    server_thread.join()