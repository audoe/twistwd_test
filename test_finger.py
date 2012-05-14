from twisted.protocols import finger

from twisted.internet import protocol,reactor
class FingerFactory(protocol.ServerFactory):
    protocol=finger.Finger
    def getUser(self,user):
        return 'ds'
reactor.listenTCP(1079,FingerFactory())
reactor.run()
