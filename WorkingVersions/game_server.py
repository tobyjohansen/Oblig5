import socket
import threading
import time

server_ip = '127.0.0.1'
server_port = 5555


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


class ConnThread(threading.Thread):
    def __init__(self, threadID, name, conn, addr):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.name = name
        self.addr = addr
        self.conn = conn
        self.p1_position = ""
        self.p2_position = ""

    def run(self):
        p1_position = ()
        p2_position = ()
        print(f"Starting threadname: {self.name}, ThreadID: {self.threadID}")
        print(f"connected by {self.addr}")
        msg = str(self.threadID).encode("utf_8")
        self.conn.send(msg)
        while True:
            data = self.conn.recv(1024)
            if not data:
                break

            # Get player positions and upgdate
            if self.threadID == 0:
                p1_position = data.decode("utf_8")
                print(f"p1 Position is: {self.p1_position}")
            if self.threadID == 1:
                p2_position = data.decode("utf_8")
                print(f"p2 Position is: {self.p2_position}")

            # Send player position to clients
            if self.threadID == 0:
                message_p2_position_data = str(p2_position)
                msg_p2_pd = message_p2_position_data.encode("utf_8")
                self.conn.send(msg_p2_pd)
                print("Sendt p2 positon to p1")
            if self.threadID == 1:
                message_p1_position_data = str(p1_position)
                msg_p1_pd = message_p1_position_data.encode("utf_8")
                self.conn.send(msg_p1_pd)



            self.conn.sendall(data)

            msg = data.decode("utf_8")
            print(msg)
        self.conn.close()


server = ServerNetwork(server_ip, server_port)
connID = 0

while True:
    server.listening()
    conn, addr = server.server.accept()
    x = ConnThread(connID, "NoName", conn, addr)
    x.start()
    connID += 1
