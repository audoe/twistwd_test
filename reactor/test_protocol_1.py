from twisted.internet import protocol,reactor


class FingerProtocol(protocol.Protocol):
    def connectionMade(self):   #this is rewrite??I don`t understand now!!
        self.transport.loseConnection()   #just close the connection
class FingerFactory(protocol.ServerFactory):
    protocol=FingerProtocol
reactor.listenTCP(1079,FingerFactory())  #binding the port 
reactor.run()
