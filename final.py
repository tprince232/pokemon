import pygame, math, sys
from pygame.locals import *
from connections import *
from animations import *
from twisted.python import log
from twisted.internet.task import LoopingCall


class OptionBox(pygame.sprite.Sprite):

    def __init__(self, GameSpace):
        pygame.sprite.Sprite.__init__(self)
        self.gamespace = GameSpace

        self.grass = pygame.image.load("grassLand.png")
        self.rectGrass = self.grass.get_rect()
        self.rectGrass = self.rectGrass.move(0,0)

        self.scene = pygame.image.load("battlegrass.png")
        self.rectScene = self.scene.get_rect()
        self.rectScene = self.rectScene.move(0,0)

        #GENERATE OPTION BOX
        self.box = pygame.image.load("optionBox.png")
        self.rect = self.box.get_rect()
        self.rect = self.rect.move(345,220)

    def writeText(self, size, text, w, h):
#Create OptionBox FONT (fight)
        self.myfont = pygame.font.SysFont("monospace", size)
# render text
        self.label = self.myfont.render(text, 1, (0,0,0))
        self.gamespace.screen.blit(self.label, (w, h))

    def tick(self):
        pass

class Player1(pygame.sprite.Sprite):

    def __init__(self, GameSpace, playerNum, playerPoke):
        pygame.sprite.Sprite.__init__(self)
        self.gamespace = GameSpace
        self.action = "wait"

        #GENERATE POKEMON
        if playerNum == 1:
            self.pokemon = pygame.image.load("./pokeDex/" + playerPoke + ".png")
            self.original = pygame.image.load("./pokeDex/" + playerPoke + ".png")

            self.trainer = pygame.image.load("./trainerDex/ashketchum.png")
            self.originalTrainer = pygame.image.load("./trainerDex/ashketchum.png")

        if playerNum == 2:
            self.pokemon = pygame.image.load("./pokeDex/" + playerPoke + ".png")
            self.original = pygame.image.load("./pokeDex/" + playerPoke + ".png")

            self.trainer = pygame.image.load("./trainerDex/lilboy.png")
            self.originalTrainer = pygame.image.load("./trainerDex/lilboy.png")

        self.rect = self.pokemon.get_rect()
        self.rectTrainer = self.trainer.get_rect()
        self.speed = [0,0]
        self.rect = self.rect.move(425,45)
        self.rectTrainer = self.rectTrainer.move(365,40)

    def move(self):
        self.rect.move_ip(self.speed)



    def tick(self):
        if self.action == "tackle":
            pass

class Player2(pygame.sprite.Sprite):

    def __init__(self, GameSpace, playerNum, playerPoke):
        pygame.sprite.Sprite.__init__(self)
        self.gamespace = GameSpace

        #GENERATE POKEMON
        if playerNum == 1:
            self.pokemon = pygame.image.load("./pokeDex/" + playerPoke + "back.png")
            self.original = pygame.image.load("./pokeDex/" + playerPoke + "back.png")


        if playerNum == 2:
            self.pokemon = pygame.image.load("./pokeDex/" + playerPoke + "back.png")
            self.original = pygame.image.load("./pokeDex/" + playerPoke + "back.png")


        self.rect = self.pokemon.get_rect()
        self.speed = [0,0]
        self.rect = self.rect.move(95,165)


    def move(self):
        self.rect.move_ip(self.speed)

    def tick(self):
        pass


#step 1: initializing GameSpace
class GameSpace:

    def main(self, pNum, poke):

        pygame.init()
        self.size = self.width, self.height = 650, 400
        self.black = 0,0,0
        self.screen = pygame.display.set_mode(self.size)
        pygame.display.set_caption('Pokemon Game')

        port = 46050
        if pNum == 1:
            self.fact = Player1Factory(poke, pNum)
            reactor.listenTCP(port, self.fact)
        elif pNum == 2:
            self.fact = PlayerFactory(poke, pNum)
            reactor.connectTCP("ash.campus.nd.edu", port, self.fact)

        self.playerPoke = poke
        self.otherPoke = self.playerPoke

        #step 2: initialize game objects
        self.player1 = Player1(self, pNum, self.playerPoke)
        self.player2 = Player2(self, pNum, self.otherPoke)
        self.optionBox = OptionBox(self)
        self.clock = pygame.time.Clock()
        self.player2isInit = 0

        #step 3/4 start game loop and tick regulate (with LoopingCall)
        def game_tick():

            #step 5: reading user input
            if self.player2isInit == 0:
                try:
                    print "writing!"
                    self.fact.playerConn.transport.write("getPoke")
                    if self.fact.playerConn.inp != "":
                        otherPoke = self.fact.playerConn.inp
                        self.player2 = Player2(self, pNum, otherPoke)
                        self.player2isInit = 1
                except:
                    pass

            for event in pygame.event.get():
                if event.type == KEYDOWN:
                    pass
                    #self.player.move()
                if event.type == pygame.QUIT:
                    sys.exit()
                # if event.type == pygame.MOUSEBUTTONUP:
                #     if pos[0] >
                #     pos = pygame.mouse.get_pos()
                #     print "POS: " + str(pos)


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
            self.screen.blit(self.optionBox.grass, self.optionBox.rectGrass)
            self.screen.blit(self.optionBox.scene, self.optionBox.rectScene)
            self.screen.blit(self.player1.pokemon, self.player1.rect)
            self.screen.blit(self.player2.pokemon, self.player2.rect)
            self.screen.blit(self.player1.trainer, self.player1.rectTrainer)
            self.screen.blit(self.optionBox.box, self.optionBox.rect)

            self.optionBox.writeText(30, "FIGHT", 375, 250)
            self.optionBox.writeText(30, "POKeMON", 375, 290)
            self.optionBox.writeText(30, "RUN", 375, 330)


            pygame.display.flip()

        tick = LoopingCall(game_tick)
        tick.start(1.0 / 60)

        reactor.run()

#later as part of step 1
if __name__=='__main__':
    log.startLogging(sys.stdout)

    if len(sys.argv) != 3:
        print "Invalid number of command line arguments.\nFormat: final.py <playerNum> <PokeName>"
        sys.exit(0)

    elif sys.argv[1] != "1":
        if sys.argv[1] != "2":
            print "Invalid player number.\nFormat: final.py <playerNum> <PokeName>"
            sys.exit(0)

    playerNum = int(sys.argv[1])
    playerPoke = str(sys.argv[2])

    gs = GameSpace()
    gs.main(playerNum, playerPoke)
