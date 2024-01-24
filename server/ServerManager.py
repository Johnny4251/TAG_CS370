import threading
from GameServer import GameServer
import time

COMMANDS = ["kill", "list clients", "help", "run"]

def create_server():
    server = GameServer(debug=False)
    server_thread = threading.Thread(target=server.run)
    return server, server_thread

if __name__ == "__main__":
    server, server_thread = create_server()

    time.sleep(1) # give thread a sec to catch up
    cmd = ""
    while cmd != COMMANDS[0]: # kill
        cmd = input("@TagServer>> ")
        if cmd == COMMANDS[1]: # list clients
            print(server.clients_conns.keys())
        elif cmd == COMMANDS[2]: # help
            print("===COMMANDS===")
            for command in COMMANDS:
                print(">> " + command)
            print("==============")
        elif cmd == COMMANDS[3]: # run
            print("starting server")
            server_thread.start()
        else:
            # if statement handles bug
            if cmd != COMMANDS[0]: print("Command not found! Try >>help for help")

        time.sleep(0.5) # give thread a sec to catch up
    try:
        server.kill()
        server_thread.join()
    except Exception as e:
        print("Exception: ", e)
    print("Goodbye!")