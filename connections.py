from twisted.internet.protocol import Factory
from twisted.internet.protocol import ClientFactory
from twisted.internet.protocol import Protocol
from twisted.internet import reactor
from final import *
import sys

class Player1Connection(Protocol):
    def __init__(self, gs):
        self.connected = 0
        self.gs = GameSpace()

    def connectionMade(self):
        print "Connection made."
        self.connected = 1
        self.gs.main(1)

    def dataReceived(self, data):
        pass


class Player1Factory(Factory):
    def __init__(self, gs):
        self.player1Conn = Player1Connection(gs)

    def buildProtocol(self, addr):
        return self.player1Conn



class Player2Connection(Protocol):
    def __init__(self, gs):
        self.connected = 0
        self.gs = GameSpace()

    def connectionMade(self):
        print "Connection made."
        self.connected = 1
        self.gs.main(2)

    def dataReceived(self, data):
        pass


class Player2Factory(ClientFactory):
    def __init__(self, gs):
        self.player2Conn = Player2Connection(gs)

    def buildProtocol(self, addr):
        return self.player2Conn


def initializePlayers(playerNum, gs):
    print "Detected player num:", playerNum
    if playerNum == 1:
        factory = Player1Factory(gs)
        reactor.listenTCP(44050, factory)
        reactor.run()

    elif playerNum == 2:
        factory = Player2Factory(gs)
        reactor.connectTCP("ash.campus.nd.edu", 44050, factory)
        reactor.run()
