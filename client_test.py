import socket
import pickle

class ClientNetwork:
    def __init__(self):
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_host = "127.0.0.1"
        self.port = 5555
        self.addr = (self.server_host, self.port)

    def connect(self):
        try:
            self.client.connect(self.addr)
        except socket.error as e:
            print("Connection timed out")

    def send(self, data):
        try:
            self.client.send(data)
        except socket.error as e:
            print(e)

    def get_data(self):
        data = self.client.recv(4096*4)
        return data


'''
client = ClientNetwork()
client.connect()
client.send_data()

print('received', repr(client.get_data()))
'''
