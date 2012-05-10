from twisted.internet import protocol,reactor
class FingerProtocol(protocol.Protocol):    #protocol make the final result
    pass 
class FingerFactory(protocol.ServerFactory):  #factory make protocol
    protocol=FingerProtocol
reactor.listenTCP(1079,FingerFactory())  #listen 
reactor.run()  #run !!
#try to understand the source of the code
#don`t to do the no use thing like a lot of tmp


