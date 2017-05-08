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
            elif item.P == 2:
                if item.rect.x < item.endx or item.rect.y > item.endy:
                    self.items.remove(item)
                    self.gs.inFight = 0

class SpriteBall(pygame.sprite.Sprite):
    def __init__(self, gs, image, P, rate):
        self.image = pygame.image.load("anims/" + image)
        self.rect = self.image.get_rect()
        self.P = P
        self.rate = rate
        self.initCoords()

    def initCoords(self):
        if self.P == 1:
            self.rect.x = 300
            self.rect.y = 275
            self.dx = self.rate
            self.dy = -.75 * self.rate
            self.endx = 450
            self.endy = 100
        elif self.P == 2:
            self.rect.x = 450
            self.rect.y = 100
            self.dx = -1 * self.rate
            self.dy = .75 *self.rate
            self.endx = 300
            self.endy = 275
            
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
