import socket

class Network:
    def __init__(self):
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server = "10.171.1.91"
        self.port = 5555
        self.addr = (self.server, self.port)
        self.pos = self.connect()

    def getPos(self):
        return self.pos

    def connect(self):
        try:
            self.client.connect(self.addr)
            return  self.client.recv(2048*4).decode()
        except:
            pass

    def send(self, data):
        try:
            self.client.send(str.encode(data))
            return self.client.recv(2048*4).decode()
        except socket.error as e:
            print(e)
