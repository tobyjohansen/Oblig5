import socket

server_ip = '127.0.0.1'
server_port = 5555


class ClientNetwork:
    def __init__(self):
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.host = '127.0.0.1'
        self.port = 5555
        self.addr = (self.host, self.port)
        self.position = self.connect()

    def get_player_position(self):
        return self.position

    def connect(self):
        try:
            self.client.connect(self.addr)
            return self.client.recv(2048).decode()
        except:
            pass

    def send(self, data):
        try:
            self.client.send(str.encode(data))
            return self.client.recv(2048).decode()
        except socket.error as e:
            print(e)
