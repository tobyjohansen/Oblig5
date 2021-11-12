import socket
import threading
import time

server_ip = '127.0.0.1'
server_port = 5555

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
    s.bind((server_ip, server_port))
except socket.error as e:
    str(e)

s.listen(2)
print("Waiting for a connection, Server Started")

"""
class ServerNetwork:
    def __init__(self, host, port):
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.host = host
        self.port = port
        self.addr = (self.host, self.port)

    def listening(self):
        try:
            self.server.bind(self.addr)
            self.server.listen()
        except socket.error as e:
            str(e)
"""

class ConnThread(threading.Thread):
    def __init__(self, threadID, name, conn, addr):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.name = name
        self.addr = addr
        self.conn = conn
        self.p1_x_position = 50
        self.p2_x_position = 0

    def run(self):
        p1_position = ()
        p2_position = ()
        print(f"Starting threadname: {self.name}, ThreadID: {self.threadID}")
        print(f"connected by {self.addr}")
        msg = str(self.threadID).encode("utf_8")
        self.conn.send(msg)

        # Player Position var
        p1_x_position = 0
        while True:
            data = self.conn.recv(1024)
            if not data:
                break

            # Get player positions and upgdate
            if self.threadID == 0:
                msg = data.decode("utf_8")
                p1_x_position = str(msg)
                print(msg)

            msg = p1_x_position.encode("utf_8")
            self.conn.send(msg)
            print("ThreadID1 Testing sending msg")

        self.conn.close()



connID = 0
while True:
    conn, addr = s.accept()
    x = ConnThread(connID, "NoName", conn, addr)
    x.start()
    connID += 1
