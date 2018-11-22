# Секция импортов
import sys
from time import time
from math import sin, cos, atan2, pi, sqrt

import pygame

# Секция констант
# Тут будем хранить настройки игры

WIDTH = 800
HEIGHT = 600


WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (140, 10, 10)
GREEN = (10, 140, 10)
BLUE = (10, 10, 140)

COLORS = [WHITE, BLACK, RED, GREEN, BLUE]

FPS = 60

BULLET_SPEED = 30

# Секция описания

class State:
    def __init__(self):
        self.player = None
        self.bullets = pygame.sprite.Group()
        self.targets = pygame.sprite.Group()
        self.sc = pygame.display.set_mode((WIDTH, HEIGHT))


class Player(pygame.sprite.Sprite):
    x = 0
    y = 0
    angle_rad = 0
    fire_delay = 0
    last_fire_time = 0
    color = RED

    def __init__(self, state):
        width, height = state.sc.get_size()
        self.x = width / 30
        self.y = height / 30
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((10, 10))
        self.image.fill(self.color)
        self.rect = self.image.get_rect()
        state.player = self

    def rotate(self, mouse_coords):
        mouse_x, mouse_y = mouse_coords
        x = mouse_x - self.x
        y = mouse_y - self.y
        rads = atan2(-y,x)
        rads %= 2*pi
        self.angle_rad = rads

    def fire(self, state):
        now = time()
        velocity = (
            BULLET_SPEED * cos(self.angle_rad),
            BULLET_SPEED * sin(self.angle_rad))
        if now - self.last_fire_time > self.fire_delay:
            Bullet(self.x, self.y, velocity).add(state.bullets)
            self.last_fire_time = now 


class Bullet(pygame.sprite.Sprite):
    velocity = (0,0)
    long_range = 10000 # дальнобойность
    distance = 0
    color = GREEN

    def __init__(self, x, y, velocity):
        self.velocity = velocity
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((50, 50))
        self.image.fill(self.color)
        self.rect = self.image.get_rect(center=(x, y))

    def update(self):
        if self.distance > self.long_range:
            self.kill()
        x_vel, y_vel  = self.velocity
        self.rect.x   += x_vel
        self.rect.y   -= y_vel
        self.distance += sqrt(x_vel**2 + y_vel**2)


class Target:
    x = 0
    y = 0
    def __init__(self):
        pass


# Инициализация

def main():
    pygame.init()

    clock = pygame.time.Clock()
    state = State()
    player = Player(state)

    while 1:
        state.sc.fill(BLACK)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
        # keys = pygame.key.get_pressed()
        mouse = pygame.mouse.get_pos()
        mouse_buttons = pygame.mouse.get_pressed()
        player.rotate(mouse)
        if mouse_buttons[0]:
            player.fire(state)
        state.sc.blit(player.image,
                  (player.x - 15, player.y - 15))
        state.bullets.draw(state.sc)
        pygame.display.update()
        clock.tick(FPS)
        state.bullets.update()


if __name__ == '__main__':
    main()
