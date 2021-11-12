import socket

import pygame
import network_test


class Window:
    def __init__(self):
        self.width = 500
        self.height = 500
        self.win = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption("Client")

    def redraw(self, p1, p2):
        self.win.fill((255, 255, 255))
        p1.draw(self.win)
        p2.draw(self.win)
        pygame.display.update()


class Player():
    def __init__(self, x, y, width, height, color):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.color = color
        self.rect = (x,y,width,height)
        self.pyrect = pygame.Rect(self.rect)
        self.vel = 3

    def draw(self, win):
        pygame.draw.rect(win, self.color, self.rect)

    def controls(self):
        keys = pygame.key.get_pressed()

        if keys[pygame.K_LEFT]:
            self.x -= self.vel

        if keys[pygame.K_RIGHT]:
            self.x += self.vel

        if keys[pygame.K_UP]:
            self.y -= self.vel

        if keys[pygame.K_DOWN]:
            self.y += self.vel

        self.update()

    def update(self):
        self.rect = (self.x, self.y, self.width, self.height)
        self.pyrect = pygame.Rect(self.rect)


def read_position(str):
    str = str.split(",")
    return int(str[0]), int(str[1])


def make_position(tup):
    return str(tup[0]) + "," + str(tup[1])


"""
def redrawWindow(win,player, player2):
    win.fill((255,255,255))
    player.draw(win)
    player2.draw(win)
    pygame.display.update()
"""


def main():
    # Initialise pygame and pygame window
    pygame.init()
    win = Window()

    # Establish connection with the server
    network = network_test.ClientNetwork()

    # Get first starting position from the server
    player_starting_position = read_position(network.get_player_position())

    # Creates the player objects
    p = Player(player_starting_position[0], player_starting_position[1], 25, 100, (0, 255, 0))
    p2 = Player(0, 0, 25, 100, (255, 0, 0))

    # Gets the client number from server
    try:
        data = network.client.recv(10264)
    except socket.error as e:
        str(e)
    player_number = int(data.decode("utf_8"))
    print(player_number)

    # Creates pygame clock
    clock = pygame.time.Clock()

    while True:
        # Sets the frame rate of the game
        clock.tick(60)

        # Updates the other player position position
        player2_position = read_position(network.send(make_position((p.x, p.y))))
        p2.x = player2_position[0]
        p2.y = player2_position[1]
        p2.update()

        # Events for quit button
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()

        # Player Movement border
        # P1
        if player_number == 0:
            if p.pyrect.right >= (win.width / 2):
                p.x = int((win.width / 2) - 25)
            if p.pyrect.left <= 0:
                p.x = 0
            if p.pyrect.bottom >= win.height:
                p.y = win.height - 100
            if p.pyrect.top <= 0:
                p.y = 0
        # P2
        if player_number == 1:
            if p.pyrect.left <= (win.width / 2):
                p.x = int((win.width / 2))
            if p.pyrect.right >= win.width:
                p.x = win.width - 25
            if p.pyrect.bottom >= win.height:
                p.y = win.height - 100
            if p.pyrect.top <= 0:
                p.y = 0

        # Establishes controls
        p.controls()

        # Redraws the window
        win.redraw(p, p2)

main()
