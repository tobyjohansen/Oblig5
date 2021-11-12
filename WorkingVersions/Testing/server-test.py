import socket
from _thread import *
import server_gui

server_ip = "127.0.0.1"
port = 5555

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
    server.bind((server_ip, port))
except socket.error as e:
    str(e)

server.listen(2)
print("Waiting for a connection with a client...")


#Code from techwithtim
def read_pos(str):
    str = str.split(",")
    return int(str[0]), int(str[1])

def make_pos(tup):
    return str(tup[0]) + "," + str(tup[1])


# Set player Starting Position
pos = [(50, 200),(350, 200),(200, 200)]


# This is the code that is running in the thread
def thread_client(conn, connID):

    # Sends starting position to the client
    conn.send(str.encode(make_pos(pos[connID])))
    answer = ""

    # Sends client number to the client
    msg = str(connID).encode("utf_8")
    conn.send(msg)

    # Main loop of the thread
    while True:
        try:
            data = read_pos(conn.recv(2048).decode())
            pos[connID] = data

            if not data:
                break
            else:
                if connID == 1:
                    reply = pos[0] + pos[2]
                else:
                    reply = pos[1] + pos[2]

                print("Received: ", data)
                print("Sending : ", reply)

            conn.sendall(str.encode(make_pos(reply)))
        except:
            break
    print("Lost connection")
    conn.close()


# Set variables
connID = 0

# Accepts connection and starts a new thread for each connection
while True:
    conn, addr = server.accept()
    start_new_thread(thread_client, (conn, connID))
    connID += 1

