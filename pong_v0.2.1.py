import pygame
import os
import random

pygame.init()  # init pygame and pygame.font
pygame.font.init()

fps = 60  # fps limit

sc_size = (800, 600)  # screen size

ball_size = (50, 50)
ball_x_change = 5
ball_y_change = -5

board_size = (150, 30)
board_x_change = 0

colors = {                  # colors for screen
    'ball': (0, 255, 255),
    'bg': (0, 0, 0),
    'board': (0, 128, 128)
}

points = 0

is_save = False
is_res = False


class Ball(pygame.sprite.Sprite):  # sprite of ball
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load('ball.png')
        self.rect = self.image.get_rect()
        self.rect.center = (random.randint(75, sc_size[0] - 75), random.randint(75, sc_size[1] - 75))

    def update(self):  # move ball
        self.rect.x += ball_x_change
        self.rect.y += ball_y_change


class Board(pygame.sprite.Sprite):  # sprite of board
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface(board_size)
        self.image.fill(colors['board'])
        self.rect = self.image.get_rect()
        self.rect.center = (sc_size[0] / 2, 50)

    def update(self):  # move board
        self.rect.x += board_x_change
        self.rect.y = sc_size[1] - 50


def save():  # create save file and write result
    global is_save
    if not os.path.exists('C:/Users/' + os.getlogin() + '/Documents/My Games'):  # create path to save dir
        os.mkdir('C:/Users/' + os.getlogin() + '/Documents/My Games')
    if not os.path.exists('C:/Users/' + os.getlogin() + '/Documents/My Games/Pong'):
        os.mkdir('C:/Users/' + os.getlogin() + '/Documents/My Games/Pong')
    if not os.path.isfile('C:/Users/' + os.getlogin() + '/Documents/My Games/Pong/info.txt'):
        info = open('C:/Users/' + os.getlogin() + '/Documents/My Games/Pong/info.txt', 'w+')  # create info.txt file
        info.close()
    info = open('C:/Users/' + os.getlogin() + '/Documents/My Games/Pong/info.txt', 'a+')  # open info.txt file
    info.write(str(points) + ',')  # add result
    info.close()
    info_text = open('C:/Users/' + os.getlogin() + '/Documents/My Games/Pong/info.txt', 'r+').read()
    info_text = info_text.split(',')
    info_text.remove('')
    info_lint = list(map(int, info_text))
    info_lint.sort(reverse=True)
    info_text = list(map(str, info_lint))
    info_str = ','.join(info_text[0:8]) + ','
    info = open('C:/Users/' + os.getlogin() + '/Documents/My Games/Pong/info.txt', 'w+')
    info.write(info_str)
    info.close()
    is_save = True


def results():
    global is_res
    info = open('C:/Users/' + os.getlogin() + '/Documents/My Games/Pong/info.txt', 'r+')
    info_text = info.read().split(',')
    return info_text
    is_res = True


def move():  # makes the move in game
    global ball_x_change, ball_y_change, points, board_x_change
    if board.rect.right >= sc_size[0]:  # does not allow the board to go beyond the borders
        board_x_change = 0
        board.rect.right = sc_size[0] - 1
    elif board.rect.left <= 0:
        board_x_change = 0
        board.rect.left = 1

    if ball.rect.right >= sc_size[0] or ball.rect.left <= 0:  # bouncing of borders
        ball_x_change *= -1
        points += 10
    if ball.rect.top <= 0:
        ball_y_change *= -1
        points += 10

    if ball.rect.colliderect(board):  # bouncing of board
        if abs(board.rect.top - ball.rect.bottom) <= 10 and ball_y_change > 0:
            ball_y_change *= -1
            points += 10
        if abs(board.rect.bottom - ball.rect.top) <= 10 and ball_y_change < 0:
            ball_y_change *= -1
            points += 10
        if abs(board.rect.left - ball.rect.right) <= 10 and ball_x_change > 0:
            ball_x_change *= -1
            points += 10
        if abs(board.rect.right - ball.rect.left) <= 10 and ball_x_change < 0:
            ball_x_change *= -1
            points += 10


def restart():
    global resulting, gaming, ball_y_change, points, is_save
    resulting = False
    gaming = True
    is_save = False
    ball.rect.center = (random.randint(55, sc_size[0] - 5), random.randint(55, sc_size[1] - 5))
    board.rect.center = (sc_size[0] / 2, 50)
    ball_y_change = abs(ball_y_change) * -1
    points = 0


sc = pygame.display.set_mode(sc_size)  # create screen
clock = pygame.time.Clock()  # create fps lock
all_sprites = pygame.sprite.Group()  # create group of all sprites
board = Board()  # make class into variable
ball = Ball()  # make class into variable
all_sprites.add(ball)  # add sprites in groups
all_sprites.add(board)

f1 = pygame.font.Font(None, 32)

resulting = False
gaming = True
running = True
while running:
    clock.tick(fps)
    for e in pygame.event.get():  # events
        if e.type == pygame.QUIT:  # close game
            running = False

        if e.type == pygame.KEYDOWN:  # all clicks
            if e.key == pygame.K_a and board.rect.left >= 0:
                board_x_change = -5
            if e.key == pygame.K_d and board.rect.right <= sc_size[0]:
                board_x_change = 5
            if e.key == pygame.K_r:
                restart()
                continue
            if e.key == pygame.K_p:
                pass

        if e.type == pygame.KEYUP:
            if e.key == pygame.K_a or e.key == pygame.K_d:
                board_x_change = 0
    sc.fill(colors['bg'])
    if gaming:
        move()
        all_sprites.update()
        all_sprites.draw(sc)
        if ball.rect.y > sc_size[1]:
            gaming = False
            resulting = True
    elif resulting:
        save()
        if not is_res:
            texts = results()
        y = 20
        sc.blit(pygame.font.Font(None, 36).render('Лучшие результаты:', True, (255, 255, 255)), (50, 20))
        sc.blit(pygame.font.Font(None, 30).render('R - рестарт', True, (255, 255, 255)), (50, sc_size[1] - 50))
        sc.blit(pygame.font.Font(None, 30).render('Сейчас ваш результат - ' + str(points), True,\
                                                  (255, 255, 255)), (50, sc_size[1] - 80))
        texts.remove('')
        for j in texts:
            text = f1.render(j, True, (255, 255, 255))
            y += 30
            if y < sc_size[1] - 200:
                    sc.blit(text, (50, y))

    pygame.display.update()
