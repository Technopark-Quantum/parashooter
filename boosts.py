import pygame 
import random
from math import sin, cos, atan2, pi, sqrt
from settings import *
from lib import get_angle, get_velocity

class Boost(pygame.sprite.Sprite):
    def __init__(self, state,x,y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(self.image_path)
        self.rect = self.image.get_rect()
        state.boosts.add(self) 
        self.rect.x = x
        self.rect.y = y
 
class Heal(Boost):
    image_path = 'images/boosts/heal.png'
    
    def activate(self, state):
        state.player.hp += 5
        self.kill()	
       

class Speed(Boost):
    image_path = 'images/boosts/bread.png'
    
    def activate(self, state):
        state.player.move_speed += 0.5
        self.kill()	
		
class FireDelay(Boost):
    image_path = 'images/boosts/coin.png'
    
    def activate(self, state):
        state.player.fire_delay *= 0.8
        self.kill()			

