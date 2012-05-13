from twisted.internet.protocol import Protocol,ClientCreator
from twisted.web import proxy, http

from twisted.internet import reactor
from twisted.protocols.basic import LineReceiver
from twisted.internet.protocol import Factory,ClientFactory
class Transfer(Protocol):
        def __init__(self):
                pass
        def connectionMade(self):
                c = ClientCreator(reactor,Clienttransfer)
                c.connectTCP("127.0.0.1",8080).addCallback(self.set_protocol)
                self.transport.pauseProducing()

        def set_protocol(self,p):
                self.server = p
                p.set_protocol(self)

        def dataReceived(self,data):
                self.server.transport.write(data)

        def connectionLost(self,reason):
                self.transport.loseConnection()
                self.server.transport.loseConnection()

class Clienttransfer(Protocol):
        def __init__(self):
                pass

        def set_protocol(self,p):
                self.server = p
                self.server.transport.resumeProducing()
                pass
        def dataReceived(self,data):
                self.server.transport.write(data)
                pass

factory = Factory()
factory.protocol = Transfer
reactor.listenTCP(1099,factory)


class ProxyFactory(http.HTTPFactory):
    def buildProtocol(self, addr):
        return proxy.Proxy()
 
reactor.listenTCP(8080, ProxyFactory())
reactor.run()
