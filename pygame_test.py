import pygame
import client_test
import pickle


class Window:
    def __init__(self):
        self.width = 500
        self.height = 500
        self.win = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption("Client")

    def redraw(self, player, player2):
        self.win.fill((255, 255, 255))
        player.draw(self.win)
        player2.draw(self.win)
        pygame.display.update()


class Player:
    def __init__(self, x, y, width, height, color):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.color = color
        self.rect = (x, y, width, height)
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

        self.rect = (self.x, self.y, self.width, self.height)


'''
def main():
    run = True
    win = Window()
    p = Player(50,50,100,100,(0,255,0))
    clock = pygame.time.Clock()

    while run:
        clock.tick(60)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()
        p.controls()
        win.redraw(p)
'''

if __name__ == '__main__':
    pygame.init()
    win = Window()
    test_client = client_test.ClientNetwork()
    test_client.connect()

    current_player = 0
    p1 = Player(50, 200, 25, 55, (0, 255, 0))
    p2 = Player(400, 200, 25, 55, (255, 0, 0))

    data = test_client.get_data()
    message = pickle.loads(data)
    if message == "player1":
        print("player1")
        current_player = 1
    elif message == "player2":
        print("player2")
        current_player = 2
    else:
        print("Finished choosing players")

    clock = pygame.time.Clock()
    while True:
        if current_player == 1:
            while True:
                clock.tick(60)
                #Send your players current possition to server
                test = p1.rect
                position = pickle.dumps(test)
                test_client.send(position)

                #Retrieves the other players current possition from server
                data = test_client.get_data()
                message = pickle.loads(data)
                print(f"player 2 position is: {message}")

                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()

                p1.controls()
                win.redraw(p1, p2)
        elif current_player == 2:
            while True:
                clock.tick(60)
                # Send your players current possition to server
                test = p2.rect
                position = pickle.dumps(test)
                test_client.send(position)

                # Retrieves the other players current possition from server
                data = test_client.get_data()
                message = pickle.loads(data)
                print(f"player 1 position is: {message}")

                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()

                p2.controls()
                win.redraw(p1, p2)
        else:
            break



        '''
        data = test_client.get_data()
        message = pickle.loads(data)
        print(message)
        '''

        '''
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
        p1.controls()
        win.redraw(p1, p2)
        '''
