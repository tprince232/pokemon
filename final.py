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

    def writeText(self, size, text, w, h, color):
#Create OptionBox FONT (fight)
        self.myfont = pygame.font.SysFont("monospace", size)
# render text
        self.label = self.myfont.render(text, 1, color)
        self.gamespace.screen.blit(self.label, (w, h))

    def tick(self):
        pass

class Player2(pygame.sprite.Sprite):

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

        if playerPoke == "Charmander":
            self.specialMove = "Flamethrower"
            self.damage = 35
        elif playerPoke == "Bulbasaur":
            self.specialMove = "Razor Leaf"
            self.damage = 40
        elif playerPoke == "Squirtle":
            self.specialMove = "Hydroblast"
            self.damage = 40
        else:
            self.specialMove = "Hyper Beam"
            self.damage = 20

    def move(self):
        self.rect.move_ip(self.speed)



    def tick(self):
        if self.action == "tackle":
            pass

    def Death(self, isDead):
        if isDead == True:
            self.pokemon = pygame.image.load("./pokeDex/" + "tombstone" + ".png")
            self.rect = self.rect.move(440,55)

    def writeText(self, size, text, w, h, color):
#Create OptionBox FONT (fight)
        self.myfont = pygame.font.SysFont("monospace", size)
# render text
        self.label = self.myfont.render(text, 1, color)
        self.gamespace.screen.blit(self.label, (w, h))



class Player1(pygame.sprite.Sprite):

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
        self.rect = self.rect.move(20,150)

        if playerPoke == "Charmander":
            self.specialMove = "Flamethrower"
            self.damage = 35
        elif playerPoke == "Bulbasaur":
            self.specialMove = "Razor Leaf"
            self.damage = 40
        elif playerPoke == "Squirtle":
            self.specialMove = "Hydroblast"
            self.damage = 40
        else:
            self.specialMove = "Hyper Beam"
            self.damage = 20

    def move(self):
        self.rect.move_ip(self.speed)

    def tick(self):
        pass

    def Death(self, isDead):
        if isDead == True:
            self.pokemon = pygame.image.load("./pokeDex/" + "tombstone" + ".png")
            self.rect = self.rect.move(40,150)

    def writeText(self, size, text, w, h, color):
#Create OptionBox FONT (fight)
        self.myfont = pygame.font.SysFont("monospace", size)
# render text
        self.label = self.myfont.render(text, 1, color)
        self.gamespace.screen.blit(self.label, (w, h))

#step 1: initializing GameSpace
class GameSpace:

    def main(self, pNum, poke):
        pygame.init()
        self.size = self.width, self.height = 650, 400
        self.black = 0,0,0
        self.screen = pygame.display.set_mode(self.size)
        pygame.display.set_caption('Pokemon Game')

        port = 40321
        if pNum == 1:
            self.fact = PlayerFactory(pNum, poke)
            reactor.listenTCP(port, self.fact)
        elif pNum == 2:
            self.fact = PlayerCFactory(pNum, poke)
            reactor.connectTCP("ash.campus.nd.edu", port, self.fact)

        self.playerPoke = poke
        self.otherPoke = self.playerPoke

        #step 2: initialize game objects
        self.player1 = Player1(self, pNum, self.playerPoke)
        self.player2 = Player2(self, pNum, self.otherPoke)
        self.players = [self.player1, self.player2]
        self.optionBox = OptionBox(self)
        self.clock = pygame.time.Clock()
        self.player2isInit = 0
        self.showMove = 0
        self.inFight = 0 #0 or no fight, 1 for self fight, 2 for opp fight
        self.stream = SpriteContainer(self)
        self.tackleColor = (0,0,0)
        self.specialColor = (0,0,0)
        self.runColor = (0,0,0)
        self.healthP1 = 140
        self.healthP2 = 140
        self.tackle = 10
        self.hydroblast = 35
        self.razorleaf = 30
        self.flamethrower = 30
        self.hyperbeam = 20
        self.RIP1 = False
        self.RIP2 = False
        self.HP1Color = (0,0,0)
        self.HP2Color = (0,0,0)
        #HP Text postions
        self.healthP1TextX = 5
        self.healthP1TextY = 225
        self.healthP2TextX = 475
        self.healthP2TextY = 30

        #step 3/4 start game loop and tick regulate (with LoopingCall)
        def game_tick():

            #step 5: reading user input
            if self.player2isInit == 0:
                try:
                    self.fact.playerConn.transport.write("getPoke")
                    if self.fact.playerConn.inp != "":
                        otherPoke = self.fact.playerConn.inp
                        self.player2 = Player2(self, pNum, otherPoke)
                        self.player2isInit = 1
                        self.resetInp()
                        self.players = [self.player1, self.player2]
                except:
                    pass

            for event in pygame.event.get():
                if event.type == KEYDOWN:
                    pass
                    #self.player.move()
                if event.type == pygame.QUIT:
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONUP:
                    pos = pygame.mouse.get_pos()
                    if pos[0] > 374 and pos[0] < 474:
                        if pos[1] >= 250 and pos[1] < 290:
                            self.tackleColor = (255,0,0)
                            self.specialColor = (0,0,0)
                            self.runColor = (0,0,0)
                            print "TACKLE clicked"
                            print "POS: " + str(pos)

                        if pos[1] >= 290 and pos[1] < 330:
                            self.tackleColor = (0,0,0)
                            self.specialColor = (255,0,0)
                            self.runColor = (0,0,0)
                            print "SPECIAL clicked"
                            print self.player1.specialMove
                            print "Damage: " + str(self.player1.damage)
                            print self.player2.specialMove
                            print "Damage: " + str(self.player2.damage)
                            # print "POS: " + str(pos)
                            self.inFight = 1
                            self.fact.playerConn.transport.write("special")

                            if self.player1.specialMove == "Hydroblast":
                                self.healthP2 = self.healthP2 - self.hydroblast
                            elif self.player1.specialMove == "Razor Leaf":
                                self.healthP2 = self.healthP2 - self.razorleaf
                            elif self.player1.specialMove == "Flamethrower":
                                self.healthP2 = self.healthP2 - self.flamethrower
                            else:
                                self.healthP2 = self.healthP2 - self.hyperbeam


                        if pos[1] >= 330 and pos[1] < 370:
                            self.tackleColor = (0,0,0)
                            self.specialColor = (0,0,0)
                            self.runColor = (255,0,0)
                            print "RUN clicked"
                            RUNNING = False
                            # print "POS: " + str(pos)
                else:
                    self.tackleColor = (0,0,0)
                    self.specialColor = (0,0,0)
                    self.runColor = (0,0,0)

            #print self.inFight
            if self.fact.playerConn.inp == "special":
                self.inFight = 2
                self.resetInp()
                if self.player2.specialMove == "Hydroblast":
                    self.healthP1 = self.healthP1 - self.hydroblast
                elif self.player2.specialMove == "Razor Leaf":
                    self.healthP1 = self.healthP1 - self.razorleaf
                elif self.player2.specialMove == "Flamethrower":
                    self.healthP1 = self.healthP1 - self.flamethrower
                else:
                    self.healthP1 = self.healthP1 - self.hyperbeam
                #elf.fact.playerConn.inp == ""

            #print self.fact.playerConn.inp

            keys = pygame.key.get_pressed()

            if keys[K_DOWN]:
                self.player1.speed[1] = 10
            if keys[K_UP]:
                self.player1.speed[1] = -10
            if keys[K_RIGHT]:
                self.player1.speed[0] = 10
            if keys[K_LEFT]:
                self.player1.speed[0] = -10


            if self.inFight != 0:
                if self.players[self.inFight-1].specialMove == "Hydroblast":
                    self.stream.enter(Hydroblast(self, self.inFight))
                elif self.players[self.inFight-1].specialMove == "Razor Leaf":
                    self.stream.enter(RazorLeaf(self, self.inFight))
                elif self.players[self.inFight-1].specialMove == "Flamethrower":
                    self.stream.enter(FlameThrower(self, self.inFight))
                else:
                    self.stream.enter(Hyperbeam(self, self.inFight))


            if self.healthP1 <= 0:
                self.RIP1 = True
                self.player1.Death(self.RIP1)
                self.HP1Color = (255,0,0)
                self.healthP1 = str(self.healthP1)
                self.healthP1 = "DEFEATED"
                self.healthP1TextX = 25
                self.healthP1TextY = 245
            if self.healthP2 <= 0:
                self.RIP2 = True
                self.player2.Death(self.RIP2)
                self.HP2Color = (255,0,0)
                self.healthP2 = str(self.healthP2)
                self.healthP2 = "DEFEATED"
                self.healthP2TextX = 390
                self.healthP2TextY = 5

            self.player1.move()
            self.player1.speed = [0,0]
            self.player2.move()
            self.player2.speed = [0,0]

#step 6: for every sprite/game object, call tick()


            self.player1.tick()
            self.player2.tick()
            self.optionBox.tick()
            self.stream.tick()

            #step 7: update the screen
            self.screen.fill(self.black)
            self.screen.blit(self.optionBox.grass, self.optionBox.rectGrass)
            self.screen.blit(self.optionBox.scene, self.optionBox.rectScene)
            if self.player2isInit == 1:
                self.screen.blit(self.player2.pokemon, self.player2.rect)
                self.screen.blit(self.player2.trainer, self.player2.rectTrainer)
            self.screen.blit(self.optionBox.box, self.optionBox.rect)

            for item in self.stream.items:
                self.screen.blit(item.image, item.rect)

            self.screen.blit(self.player1.pokemon, self.player1.rect)

            self.optionBox.writeText(30, "TACKLE", 375, 250,self.tackleColor)
            self.optionBox.writeText(30, "SPECIAL", 375, 290,self.specialColor)
            self.optionBox.writeText(30, "RUN", 375, 330,self.runColor)

            self.player1.writeText(30, "HP: " + str(self.healthP1), self.healthP1TextX, self.healthP1TextY,self.HP1Color)
            self.player2.writeText(30, "HP: " + str(self.healthP2), self.healthP2TextX, self.healthP2TextY, self.HP2Color)

            #if self.showMove == 1:
            #    pass
                # self.optionBox.writeText(40,str(self.player1.specialMove) , 75, 75)

            pygame.display.flip()

        tick = LoopingCall(game_tick)
        tick.start(1.0 / 60)

        reactor.run()

    def resetInp(self):
        self.fact.playerConn.inp = ""


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
