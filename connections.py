from twisted.internet.protocol import Factory
from twisted.internet.protocol import ClientFactory
from twisted.internet.protocol import Protocol
from twisted.internet import reactor
import sys

class Player1Connection(Protocol):
    def __init__(self):
        self.connected = 0
    
    def connectionMade(self):
        self.connected = 1

    def dataReceived(self, data):
        pass


class Player1Factory(Factory):
    def __init__(self):
        self.player1Conn = Player1Connection()

    def buildProtocol(self, addr):
        return self.player1Conn



class Player2Connection(Protocol):
    def connectionMade(self):
        pass
                    
    def dataReceived(self, data):
        pass


class Player2Factory(ClientFactory):
    def __init__(self):
        self.player2Conn = Player2Connection()
        
    def buildProtocol(self, addr):
        return self.player2Conn


def initializePlayers(playerNum):
    print "Detected player num:", playerNum
    if playerNum == 1:
        print "Detected player 1."
        factory = Player1Factory()
        reactor.listenTCP(40050, factory)
        conn = factory.player1Conn
        while conn.connected == 0:
            conn = factory.player1Conn
            
        return conn

    elif playerNum == 2:
        #try:
        factory = Player2Factory()
        reactor.connectTCP("ash.campus.nd.edu", 40050, factory)
        #except:
        #    print "Connection to player 1 failed."
        #    print "Be sure to run player 1 first."
        #    sys.exit()
        conn = factory.player2Conn

        return conn
