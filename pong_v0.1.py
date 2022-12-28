import pygame
import random

fps = 60
sc_width = 800
sc_height = 600
is_ball_up = True
is_ball_right = True

ball_width = 50
ball_height = 50
ball_x_change = 5
ball_y_change = -5

board_width = 150
board_height = 30
board_x_change = 0

points = 0

colors = {
    'ball': (0, 255, 255),
    'bg': (0, 0, 0),
    'board': (0, 128, 128)
}


class Ball(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((ball_width, ball_height))
        self.image.fill(colors['ball'])
        self.rect = self.image.get_rect()
        self.rect.center = (ball_width, ball_height)

    def update(self):
        self.rect.x += ball_x_change
        self.rect.y += ball_y_change


class Board(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((board_width, board_height))
        self.image.fill(colors['board'])
        self.rect = self.image.get_rect()
        self.rect.center = (board_width, board_height)

    def update(self):
        self.rect.x += board_x_change
        self.rect.y = sc_height - 50


pygame.init()

sc = pygame.display.set_mode((sc_width, sc_height))
clock = pygame.time.Clock()
all_sprites = pygame.sprite.Group()
balls = pygame.sprite.Group()
board = Board()
ball = Ball()
all_sprites.add(ball)
all_sprites.add(board)
balls.add(ball)

running = True
while running:
    if ball.rect.y >= sc_height + 10:
        running = False
    clock.tick(fps)

    for e in pygame.event.get():
        if e.type == pygame.QUIT:
            running = False
        elif e.type == pygame.KEYDOWN:
            if e.key == pygame.K_a:
                board_x_change = -5
            elif e.key == pygame.K_d:
                board_x_change = 5
        elif e.type == pygame.KEYUP:
            if e.key == pygame.K_a:
                board_x_change = 0
            elif e.key == pygame.K_d:
                board_x_change = 0

    if ball.rect.x >= sc_width - ball_width / 2 - 20 or ball.rect.x <= 0:
        ball_x_change *= -1
    elif ball.rect.y <= 0:
        ball_y_change *= -1
    hits = pygame.sprite.spritecollide(board, balls, False)
    if hits:
        ball_y_change *= -1
        points += 10
    sc.fill(colors['bg'])
    all_sprites.update()
    all_sprites.draw(sc)
    pygame.display.update()
print("points - " + str(points))
