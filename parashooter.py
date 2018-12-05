# Секция импортов
import sys
import random
from time import time
from math import sin, cos, atan2, pi, sqrt

import pygame

# Секция констант
# Тут будем хранить настройки игры

WIDTH = 1000
HEIGHT = 1000


WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (140, 10, 10)
GREEN = (10, 140, 10)
BLUE = (10, 10, 140)
YELLOW = (255, 227, 0)


COLORS = [WHITE, BLACK, RED, GREEN, BLUE]

FPS = 60

BULLET_SPEED = 5

# Секция описания

class State:
    def __init__(self):
        self.last_spawn = 0
        self.player = None
        self.bullets = pygame.sprite.Group()
        self.enemies = pygame.sprite.Group()
        self.sc = pygame.display.set_mode((WIDTH, HEIGHT))


class Player(pygame.sprite.Sprite):
    angle_rad = 0


    fire_delay = 0.05
    last_fire_time = 0
    color = GREEN
    hp = 10
    scores = 0


    def __init__(self, state):
        width, height = state.sc.get_size()
        pygame.sprite.Sprite.__init__(self)

        self.image = pygame.image.load('images/hero.png')
        self.image.set_colorkey((255, 255, 255))

        self.rect = self.image.get_rect()
        self.rect.x = width / 2
        self.rect.y = height / 2
        state.player = self

    def rotate(self, mouse_coords):
        mouse_x, mouse_y = mouse_coords
        x = mouse_x - self.rect.x
        y = mouse_y - self.rect.y
        rads = atan2(-y,x)
        rads %= 2*pi
        self.angle_rad = rads
        
    def move(self, x, y):
        self.rect.x = self.rect.x + x
        self.rect.y = self.rect.y + y
        

    def fire(self, state):
        now = time()
        velocity = (
            BULLET_SPEED * cos(self.angle_rad),
            BULLET_SPEED * sin(self.angle_rad))
        if now - self.last_fire_time > self.fire_delay:
            Bullet(self.rect.x, self.rect.y, velocity).add(state.bullets)
            self.last_fire_time = now



class Bullet(pygame.sprite.Sprite):
    velocity = (0,0)

    long_range = 400 # дальнобойность

    distance = 0
    color = YELLOW

    def __init__(self, x, y, velocity):
        self.velocity = velocity
        pygame.sprite.Sprite.__init__(self)

        self.image = pygame.Surface((2, 2))

        self.image.fill(self.color)
        self.rect = self.image.get_rect(center=(x, y))

    def update(self):
        if self.distance > self.long_range:
            self.kill()
        x_vel, y_vel  = self.velocity
        self.rect.x   += x_vel
        self.rect.y   -= y_vel
        self.distance += sqrt(x_vel**2 + y_vel**2)


class Enemy(Player):

    x = 0
    y = 50
    color = RED
    def __init__(self, state):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((30, 30))
        images = ['images/enemy/fox.png', 'images/enemy/bear.png', 'images/enemy/hare.png']
        image = random.choice(images)
        self.image = pygame.image.load(image)
        self.rect = self.image.get_rect()
        state.enemies.add(self)
        self.x = random.randint(1, 1000)
        self.rect.x = self.x
        self.rect.y = self.y
      
spawn_delay = 5
# last_spawn  = 0

def spawn(state):
	now = time()
	delta = now - state.last_spawn
	if delta >= spawn_delay:
		Enemy(state)
		state.last_spawn = now
		

	
	  

def main():
    pygame.init()

    clock = pygame.time.Clock()
    state = State()
    Player(state)
    font = pygame.font.SysFont('arial', 16)
    scores = font.render('Очки:' + str(state.player.scores), 1, WHITE)	
    hp = font.render('Жизни:' + str(state.player.hp), 0, WHITE)	
  
    while 1:
        state.sc.fill(BLACK)
        state.sc.blit(scores, (100, 10))
        state.sc.blit(hp, (170, 10))
        spawn(state)
        # Перехват событий
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
        keys = pygame.key.get_pressed()
        mouse = pygame.mouse.get_pos()
        mouse_buttons = pygame.mouse.get_pressed()
        state.player.rotate(mouse)
        if keys[pygame.K_w]:
            state.player.move(x=0, y=-1)
        if keys[pygame.K_a]:
            state.player.move(x=-1, y=0)
        if keys[pygame.K_s]:
            state.player.move(x=0, y=1)
        if keys[pygame.K_d]:
            state.player.move(x=1, y=0)
        if mouse_buttons[0]:
            state.player.fire(state)
        # События игры
        collisions = pygame.sprite.groupcollide(state.enemies,state.bullets,False,False)
        for enemy, bullets in collisions.items():
            enemy.kill()
            for bullet in bullets:
                bullet.kill()
        enemy_collision = pygame.sprite.spritecollideany(state.player,state.enemies)
        if enemy_collision:
             state.player.hp -= 1
	    
        
        # Отрисовка
        state.sc.blit(state.player.image,
                  (state.player.rect.x - 15, state.player.rect.y - 15))
        state.enemies.draw(state.sc)       
        state.bullets.draw(state.sc)
        pygame.display.update()
        #Условия завершения
        if state.player.hp <= 0:
            pygame.quit()
            sys.exit()
        clock.tick(FPS)
        state.bullets.update()
        

if __name__ == '__main__':
    main()
