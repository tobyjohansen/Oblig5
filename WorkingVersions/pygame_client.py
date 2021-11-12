import threading
import pygame
import game_client


class Window:
    def __init__(self):
        self.width = 500
        self.height = 500
        self.win = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption("Client")

    def redraw(self, player, player2, ball):
        self.win.fill((255, 255, 255))
        player.draw(self.win)
        player2.draw(self.win)
        ball.draw(self.win)
        pygame.display.update()


class Player:
    def __init__(self, x, y, width, height, color):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.color = color
        self.rect = (x, y, width, height)
        self.pyrect = pygame.Rect(self.rect)
        self.vel = 3
        self.x_speed = 3
        self.y_speed = 3

    def draw(self, win):
        pygame.draw.rect(win, self.color, self.rect)

    def controls(self):
        keys = pygame.key.get_pressed()

        if keys[pygame.K_LEFT]:
            self.x -= self.x_speed

        if keys[pygame.K_RIGHT]:
            self.x += self.x_speed

        if keys[pygame.K_UP]:
            self.y -= self.y_speed

        if keys[pygame.K_DOWN]:
            self.y += self.y_speed

        self.rect = (self.x, self.y, self.width, self.height)
        self.pyrect = pygame.Rect(self.rect)


class NetworkThread(threading.Thread):
    def __init__(self, threadID):
        threading.Thread.__init__(self)
        self.threadID = threadID

    def run(self):
        data = client.client.recv(1024)
        msg = data.decode("utf_8")
        print(msg)
        print("Testing")


if __name__ == '__main__':
    pygame.init()
    win = Window()

    # Open connection to the server and recieve playernumber
    client = game_client.ClientNetwork('127.0.0.1', 5555)
    client.connect()
    data = client.client.recv(1024)
    msg = data.decode("utf_8")
    playerNumber = int(msg)
    print(f"PlayerNumber: {playerNumber}")

    p1 = Player(50, 200, 25, 100, (0, 255, 0))
    p2 = Player(400, 200, 25, 100, (255, 0, 0))
    ball = Player(200, 200, 20, 20, (0, 0, 0))


    # Makes sure the color of the player are green and the other client is red
    if playerNumber == 0:
        p1.color = (0, 255, 0)
        p2.color = (255, 0, 0)
    if playerNumber == 1:
        p1.color = (255, 0, 0)
        p2.color = (0, 255, 0)

    clock = pygame.time.Clock()
    while True:

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()

        # Game Logic

        # player movement border
        #P1
        if p1.pyrect.right >= (win.width/2):
            p1.x = (win.width/2) - 25
        if p1.pyrect.left <= 0:
            p1.x = 0
        if p1.pyrect.bottom >= win.height:
            p1.y = win.height - 100
        if p1.pyrect.top <= 0:
            p1.y = 0
        #P2
        if p2.pyrect.left <= (win.width/2):
            p2.x = (win.width/2)

        # Player and ball collision
        if p1.pyrect.right >= ball.pyrect.left and p1.pyrect.top <= ball.pyrect.bottom and p1.pyrect.bottom > ball.pyrect.top and p1.pyrect.left < ball.pyrect.right:
            p1.x -= 3

        # Player Controls their rectangle
        if playerNumber == 0:
            p1.controls()
        if playerNumber == 1:
            p2.controls()

        # Network IO
        # Send player data to server
        if playerNumber == 0:
            player_x_position = p1.x
            msg = str(player_x_position).encode("utf_8")
            client.client.send(msg)
        if playerNumber == 1:
            data = client.client.recv(1024)
            msg = data.decode("utf_8")
            print(msg)
            print("Testing")
            """
            data = client.client.recv(1024)
            if not data:
                break
            msg = data.decode("utf_8")
            print(msg)
            """



        # Redraws the screen
        win.redraw(p1, p2, ball)


        # Sets the frames per seconds
        clock.tick(60)
