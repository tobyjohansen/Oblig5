import socket
import threading
import pickle

server_host = "127.0.0.1"
port = 5555


class ServerNetwork:
    def __init__(self):
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_host = "127.0.0.1"
        self.port = 5555
        self.addr = (self.server_host, port)

    def listening(self):
        try:
            self.server.bind(self.addr)
        except socket.error as e:
            str(e)
        self.server.listen()


class ServerGameLogic:
    def __init__(self):
        self.score = 0
        self.player_number = 0
        self.player1_pos = ()
        self.player2_pos = ()


class ConnThread(threading.Thread):
    def __init__(self, addr, conn, gamelogic):
        threading.Thread.__init__(self)
        self.conn = conn
        self.game = gamelogic
        self.player_number = gamelogic.player_number
        print(f"Client {addr} Connected to server")

    def run(self):
        print(f"Connection from: {addr}")
        if self.player_number == 0:
            msg = "player1"
            message = pickle.dumps(msg)
            conn.send(message)

        elif self.player_number == 1:
            msg = "player2"
            message = pickle.dumps(msg)
            conn.send(message)
        else:
            conn.close()
        while True:
            data = self.conn.recv(4096*4)
            if not data:
                print(f"Client {addr} Disconnected")
                break
            if self.player_number == 0:
                #Get player 1 position
                message = pickle.loads(data)
                self.game.player1_pos = message

                #Send player 2 position
                msg = self.game.player2_pos
                message = pickle.dumps(msg)
                conn.send(message)
            elif self.player_number == 1:
                #Get player 2 position
                message = pickle.loads(data)
                self.game.player2_pos = message

                # Send player 1 position
                msg = self.game.player1_pos
                message = pickle.dumps(msg)
                conn.send(message)
        conn.close()


server = ServerNetwork()

if __name__ == '__main__':
    server = ServerNetwork()
    game = ServerGameLogic()

    while True:
        server.listening()
        conn, addr = server.server.accept()
        newthread = ConnThread(addr, conn, game)
        newthread.start()
        game.player_number += 1
