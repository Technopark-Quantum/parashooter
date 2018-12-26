# Секция импортов
import sys
import random
from time import time
from math import sqrt

import pygame
from boosts import Heal, Speed, FireDelay
from enemies import Bear, Fox, Zayc, Spider, Boss
from settings import *
from lib import get_angle, get_velocity 




# Секция описания

class State:
    def __init__(self):
        self.boost_prob = 1  #Вероятность падения буста
        self.last_spawn = 0
        self.player = None
        self.bullets = pygame.sprite.Group()
        self.enemies = pygame.sprite.Group()
        self.boosts = pygame.sprite.Group()
        self.sc = pygame.display.set_mode((WIDTH, HEIGHT))
        self.scores = 0
    
class Player(pygame.sprite.Sprite):
    angle_rad = 0


    fire_delay = 0.05
    last_fire_time = 0
    color = GREEN
    hp = 10
    move_speed = 2


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
        rads = get_angle( mouse_coords, (self.rect.x, self.rect.y))
        self.angle_rad = rads
        
        
    def move(self, x, y):
        self.rect.x = self.rect.x + x
        self.rect.y = self.rect.y + y
        

    def fire(self, state):
        now = time()
        velocity = get_velocity(self.angle_rad,BULLET_SPEED)
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


 


spawn_delay = 2
# last_spawn  = 0

def spawn(state):
    now = time()
    delta = now - state.last_spawn
    if delta >= spawn_delay:
        enemies = [Bear, Fox, Zayc, Spider, Boss]
        enemy_class = random.choice(enemies)
        enemy_class(state)
        state.last_spawn = now
		
		

	
	  

def main():
    pygame.init()

    clock = pygame.time.Clock()
    state = State()
    Player(state)
    font = pygame.font.SysFont('arial', 16)

    while 1:
        state.sc.fill(BLACK)
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
        ms = state.player.move_speed
        if keys[pygame.K_w]:
            state.player.move(x=0, y=-ms)
        if keys[pygame.K_a]:
            state.player.move(x=-ms, y=0)
        if keys[pygame.K_s]:
            state.player.move(x=0, y=ms)
        if keys[pygame.K_d]:
            state.player.move(x=ms, y=0)
        if mouse_buttons[0]:
            state.player.fire(state)
        # События игры
        collisions = pygame.sprite.groupcollide(state.enemies,state.bullets,False,False)
        for enemy, bullets in collisions.items():
            enemy.destroy(state)
            for bullet in bullets:
                bullet.kill()
        enemy = pygame.sprite.spritecollideany(state.player,state.enemies)
        if enemy:
	        enemy.punch(state.player)
        state.bullets.update()
        state.enemies.update(state)
        # Отрисовка
        state.sc.blit(state.player.image,
                  (state.player.rect.x - 15, state.player.rect.y - 15))
        state.enemies.draw(state.sc)       
        state.bullets.draw(state.sc)
        state.boosts.draw(state.sc)
        scores = font.render('Очки:' + str(state.scores), 1, WHITE)	
        hp = font.render('Жизни:' + str(state.player.hp), 0, WHITE)	
        state.sc.blit(scores, (100, 10))
        state.sc.blit(hp, (170, 10))
        pygame.display.update()
        #Условия завершения 
        if state.player.hp <= 0:
            pygame.quit()
            sys.exit()
        clock.tick(FPS)

        

if __name__ == '__main__':
    main()
