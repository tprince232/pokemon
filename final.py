import pygame, math, sys
from pygame.locals import *

class Player(pygame.sprite.Sprite):


    def __init__(self, GameSpace):
        pygame.sprite.Sprite.__init__(self)
        self.gamespace = GameSpace

        #GENERATE DEATH STAR
        self.pokemon = pygame.image.load("Eevee.png")
        self.original = pygame.image.load("Eevee.png")
        self.rect = self.pokemon.get_rect()
        self.speed = [0,0]

    def move(self):
        self.rect.move_ip(self.speed)

    def tick(self):
        pass

#step 1: initializing GameSpace
class GameSpace:

    def main(self):
        pygame.init()
        self.size = self.width, self.height = 600, 600
        self.black = 0,0,0
        self.screen = pygame.display.set_mode(self.size)
        pygame.display.set_caption('Pokemon Game')

#step 2: initialize game objects
        self.player = Player(self)
        self.clock = pygame.time.Clock()


#step 3: start game loop
        while 1:
#step 4: tick regulation
            self.clock.tick(60)

#step 5: reading user input
            for event in pygame.event.get():
                if event.type == KEYDOWN:
                    pass
                    #self.player.move()
                if event.type == pygame.QUIT:
                    sys.exit()



            keys = pygame.key.get_pressed()

            if keys[K_DOWN]:
                self.player.speed[1] = 10
            if keys[K_UP]:
                self.player.speed[1] = -10
            if keys[K_RIGHT]:
                self.player.speed[0] = 10
            if keys[K_LEFT]:
                self.player.speed[0] = -10


            self.player.move()
            self.player.speed = [0,0]

#step 6: for every sprite/game object, call tick()


            self.player.tick()

#step 7: update the screen
            self.screen.fill(self.black)

            self.screen.blit(self.player.pokemon, self.player.rect)
            pygame.display.flip()

#later as part of step 1
if __name__=='__main__':
    gs = GameSpace()
    gs.main()
