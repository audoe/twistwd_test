from twisted.internet import protocol,reactor,defer,utils
from twisted.protocols import basic
from twisted.web import client
class FingerProcotol(basic.LineReceiver):
    def lineReceived(self,user):
        self.factory.getUser(user).addErrback(lambda _:"error")\
                                  .addCallback(lambda m:(self.transport.write(m+"\n\r")\
                                               ,self.transport.loseConnection()))
class FingerFactory(protocol.ServerFactory):
    protocol=FingerProcotol
    def __init__(self,prefix):
        self.prefix=prefix
    def getUser(self,user):
        return client.getPage(self.prefix+user)
reactor.listenTCP(1079,FingerFactory(prefix='http://baidu.com/~'))
reactor.run()
