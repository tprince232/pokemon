import pygame, math, sys
from pygame.locals import *
from twisted.python import log
from connections import *

class OptionBox(pygame.sprite.Sprite):

    def __init__(self, GameSpace):
        pygame.sprite.Sprite.__init__(self)
        self.gamespace = GameSpace

        #GENERATE GLOBE
        self.box = pygame.image.load("optionBox.png")
        self.rect = self.box.get_rect()
        self.rect = self.rect.move(345,320)

    def writeText(self, size, text, w, h):
#Create OptionBox FONT (fight)
        self.myfont = pygame.font.SysFont("monospace", size)
# render text
        self.label = self.myfont.render(text, 1, (0,0,0))
        self.gamespace.screen.blit(self.label, (w, h))

    def tick(self):
        pass

class Player1(pygame.sprite.Sprite):

    def __init__(self, GameSpace):
        pygame.sprite.Sprite.__init__(self)
        self.gamespace = GameSpace

        #GENERATE DEATH STAR
        self.pokemon = pygame.image.load("./pokeDex/Bulbasaur.png")
        self.original = pygame.image.load("./pokeDex/Bulbasaur.png")
        self.rect = self.pokemon.get_rect()
        self.speed = [0,0]
        self.rect = self.rect.move(450,75)

    def move(self):
        self.rect.move_ip(self.speed)

    def tick(self):
        pass

class Player2(pygame.sprite.Sprite):

    def __init__(self, GameSpace):
        pygame.sprite.Sprite.__init__(self)
        self.gamespace = GameSpace

        #GENERATE DEATH STAR
        self.pokemon = pygame.image.load("./pokeDex/Charzard.png")
        self.original = pygame.image.load("./pokeDex/Charzard.png")
        self.rect = self.pokemon.get_rect()
        self.speed = [0,0]
        self.rect = self.rect.move(125,275)

    def move(self):
        self.rect.move_ip(self.speed)

    def tick(self):
        pass


#step 1: initializing GameSpace
class GameSpace:

    def main(self, playerNum):
        #initializePlayers(playerNum)
        pygame.init()
        self.size = self.width, self.height = 650, 500
        self.black = 0,0,0
        self.screen = pygame.display.set_mode(self.size)
        pygame.display.set_caption('Pokemon Game')

        #connect players
        
        
#step 2: initialize game objects
        self.player1 = Player1(self)
        self.player2 = Player2(self)
        self.optionBox = OptionBox(self)
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
                self.player1.speed[1] = 10
            if keys[K_UP]:
                self.player1.speed[1] = -10
            if keys[K_RIGHT]:
                self.player1.speed[0] = 10
            if keys[K_LEFT]:
                self.player1.speed[0] = -10


            self.player1.move()
            self.player1.speed = [0,0]
            self.player2.move()
            self.player2.speed = [0,0]

#step 6: for every sprite/game object, call tick()


            self.player1.tick()
            self.player2.tick()
            self.optionBox.tick()

#step 7: update the screen
            self.screen.fill(self.black)

            self.screen.blit(self.player1.pokemon, self.player1.rect)
            self.screen.blit(self.player2.pokemon, self.player2.rect)
            self.screen.blit(self.optionBox.box, self.optionBox.rect)

            self.optionBox.writeText(30, "FIGHT", 375, 350)
            self.optionBox.writeText(30, "POKeMON", 375, 390)
            self.optionBox.writeText(30, "RUN", 375, 430)


            pygame.display.flip()

#later as part of step 1


def usage(args):
    print 'Run "' + args[0] + ' 1" if you are player 1.'
    print 'Run "' + args[0] + ' 2" if you are player 2.'
    sys.exit()

                

if __name__=='__main__':
    log.startLogging(sys.stdout)
    gs = GameSpace()
    
    if len(sys.argv) != 2:
        print "Invalid number of command line arguments."
        usage(sys.argv)

    elif sys.argv[1] != "1":
        if sys.argv[1] != "2":
            print "Invalid player number."
            usage(sys.argv)

    playerNum = int(sys.argv[1])
    initializePlayers(playerNum, gs)
    #gs.main(playerNum)
  
  
  