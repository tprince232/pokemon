import pygame, math, sys
from pygame.locals import *


class SpriteContainer():
    #holds water ball parts
    def __init__(self, gs):
        self.items = []
        self.gs = gs

    def enter(self, item):
        self.items = self.items + [item]

    def tick(self):
        for item in self.items:
            item.move()

        for item in self.items:
            if item.P == 1:
                if item.rect.x > item.endx or item.rect.y < item.endy:
                    self.items.remove(item)
                    self.gs.inFight = 0
                    #print "inFight to 0"
            elif item.P == 2:
                if item.rect.x < item.endx or item.rect.y > item.endy:
                    self.items.remove(item)
                    self.gs.inFight = 0
                    #print "inFight to 0"

class SpriteBall(pygame.sprite.Sprite):
    def __init__(self, gs, image, P, rate):
        self.image = pygame.image.load("anims/" + image)
        self.rect = self.image.get_rect()
        self.P = P
        self.rate = rate
        self.initCoords()

    def initCoords(self):
        if self.P == 1:
            self.rect.x = 200
            self.rect.y = 280
            self.dx = 1.55 * self.rate
            self.dy = -.75 * self.rate
            self.endx = 485
            self.endy = 135
        elif self.P == 2:
            self.rect.x = 480
            self.rect.y = 140
            self.dx = -1.55 * self.rate
            self.dy =   .75 *self.rate
            self.endx = 195
            self.endy = 285
            
    def move(self):
        self.rect.x = self.rect.x + self.dx
        self.rect.y = self.rect.y + self.dy


        

class Hyperbeam(SpriteBall):
    def __init__(self, gs, P):
        #super(SpriteBall, self).__init__(gs, "hbeam.jpg", P, 10)
        self.image = pygame.image.load("anims/hbeam.jpg")
        self.rect = self.image.get_rect()
        self.P = P
        self.rate = 13
        self.initCoords()
