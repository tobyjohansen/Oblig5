import socket

server_ip = '127.0.0.1'
server_port = 5555


class ClientNetwork:
    def __init__(self, host, port):
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.host = host
        self.port = port
        self.addr = (self.host, self.port)

    def connect(self):
        try:
            self.client.connect(self.addr)
        except socket.error as e:
            str(e)

    def send_data(self, message):
        message = str(message)
        msg = message.encode("utf_8")
        self.client.send(msg)

    def recieve_data(self):
        data = self.client.recv(1024)
        msg = data.decode("utf_8")
        return msg
'''
while True:
    message = str(count)
    count += 1
    msg = message.encode("utf_8")
    client.client.sendall(msg)
    data = client.client.recv(1024)
    reply = data.decode("utf_8")
    print(reply)
'''
