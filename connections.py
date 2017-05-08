from twisted.internet.protocol import Factory
from twisted.internet.protocol import ClientFactory
from twisted.internet.protocol import Protocol
from twisted.internet import reactor
import sys

class Player1Connection(Protocol):
    def __init__(self, gs, playerPoke):
        self.connected = 0
        #self.gs = GameSpace()
        self.poke = playerPoke;
        self.inp = ""

    def connectionMade(self):
        print "Connection made."
        self.connected = 1

        #self.gs.main(1, self)

    def dataReceived(self, data):
        self.imp = data


class Player1Factory(Factory):
    def __init__(self, gs, playerPoke):
        self.playerConn = PlayerConnection(gs, playerPoke)

    def buildProtocol(self, addr):
        return self.playerConn



class PlayerConnection(Protocol):
    def __init__(self, playerPoke, pNum):
        self.connected = 0
        #self.gs = GameSpace()
        self.poke = playerPoke
        self.pNum = pNum
        self.inp = ""


    def connectionMade(self):
        print "Connection made."
        self.connected = 1
        print "before launch"

    def dataReceived(self, data):
        print "Got data:", data
        if data == "getPoke":
            self.transport.write(self.poke)
        else:
            self.inp = data


class PlayerFactory(ClientFactory):
    def __init__(self, playerPoke, pNum):
        self.playerConn = PlayerConnection(playerPoke, pNum)

    def buildProtocol(self, addr):
        return self.playerConn


def initializePlayers(playerPoke, playerNum):
    print "Detected player num:", playerNum
    port = 40321
    if playerNum == 1:
        factory = PlayerFactory(playerPoke, 1)
        reactor.listenTCP(port, factory)
        reactor.run()

    elif playerNum == 2:
        factory = PlayerFactory(playerPoke, 2)
        reactor.connectTCP("ash.campus.nd.edu", port, factory)
        reactor.run()
