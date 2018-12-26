
import pygame 
import random
from math import sin, cos, atan2, pi, sqrt
from settings import *
from lib import get_angle, get_velocity
from boosts import Heal, Speed, FireDelay

class Enemy(pygame.sprite.Sprite):
    damage = 1
    throw_distance = 100
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
    def update(self, state):
        angle = get_angle((state.player.rect.x, state.player.rect.y),
                         (self.rect.x, self.rect.y))
        x_vel, y_vel  = get_velocity(angle, self.move_speed)
        self.rect.x   += x_vel
        self.rect.y   -= y_vel
    def punch(self, player):
        player.hp = player.hp - self.damage
        angle = get_angle((player.rect.x, player.rect.y), (self.rect.x, self.rect.y))
        x_vel, y_vel  = get_velocity(angle, self.throw_distance)
        player.rect.x   += x_vel
        player.rect.y   -= y_vel
    def destroy(self, state):   
        state.scores += 5
        boosts = [Heal, Speed, FireDelay]
        boost_class = random.choice(boosts)
        if state.boost_prob >= random.random():
            boost_class(state,self.rect.x,self.rect.y)
        self.kill()
		
		
 
class Bear(Enemy):
    hp = 30
    image_path = 'images/enemy/bear.png'
    

    def __init__(self, state):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(self.image_path)
        self.rect = self.image.get_rect()
        state.enemies.add(self)
        self.x = random.randint(1, WIDTH)
        self.y = random.randint(1, HEIGHT) 
        self.rect.x = self.x
        self.rect.y = self.y




class Fox(Bear):
    hp = 10
    image_path = 'images/enemy/fox.png'



class Zayc(Bear):
    hp = 5
    image_path = 'images/enemy/hare.png'

    

class Spider(Bear):
    hp = 0.0001
    image_path = 'images/enemy/spider.png'




class Boss(Bear):
    throw_distance = 500
    damage = 5
    hp = 100
    image_path = 'images/enemy/boss.png'
