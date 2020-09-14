import os
import pickle
import network

def update_servers_json(servers):
    with open('servers.pickle', 'wb') as w:
        pickle.dump(servers, w)

def get_servers():
    if not os.path.exists('servers.pickle'):
        with open('servers.pickle', 'wb') as w:
            pickle.dump({}, w)
        return {}

    with open('servers.pickle', 'rb') as w:
        try:
            return pickle.load(w)
        except:
            return {}

servers = get_servers()

def quit(connection, address):
    server.clients -= 1
    server.CLIENTS.remove(connection)
    print(f"\n[CLIENT DISCONNECTED] [{address}] Just Disconnected!")
    print(f"[ACTIVE CONNECTIONS] {server.clients}\n")

def handle_client(connection, address):
    data = b''
    while 1:
        try:
            while 1:
                packet = connection.recv(4096)
                data += packet
                try:
                    message = pickle.loads(data)
                    data = b''
                    break
                except:
                    pass

            print(f"[{address}] {message}")

            if message[0] == "QUIT":
                quit(connection, address)
                break

            elif message[0] == 'SHARE':
                servers[message[1][0]] = message[1][1]
                server.send(message, connection)
                update_servers_json(servers)

            elif message[0] == 'UPDATE':
                if message[1] not in servers:
                    servers[message[1]] = []
                server.send(['UPDATE', servers[message[1]]], connection)

        except Exception as e:
            print('Error:', e)
            quit(connection, address)
            break

    connection.close()

server = network.Server(handle_client, 5555, socket.gethostbyname(''))
