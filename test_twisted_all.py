from twisted.internet import reactor
from twisted.internet.defer import Deferred
from twisted.internet.protocol import ServerFactory,Protocol
from twisted.web import resource,server,static
from twisted.python import log
import cgi
class test_server(resource.Resource):
    def __init__(self):
        resource.Resource.__init__(self)
        self.putChild('',self)
    def getChild(self,username,request):
        text='dhsdjks<br>%s'%username
        return static.Data(text,'text/html')

class protocol_test(Protocol):
    i=0
    def connectionMade(self):
        self.transport.write('dskdjsdksdjskdjsdks')
        print 'connection is build!'
        log('dskhddksdkj')
    def dataReceived(self,data):
        if self.i>10:        
            self.transport.loseConnection()
        print data
        self.i+=1
    def connectionLost(self,reason):
        self.transport.write('sjkdhsdj')
    
class Factory_test(ServerFactory):
    protocol=protocol_test
from twisted.application import internet,service
from twisted.internet import defer
application=service.Application('finger',uid=1,gid=1)
serviceCollection = service.IServiceCollection(application)
internet.TCPServer(8000,server.Site(test_server())).setServiceParent(serviceCollection)
internet.TCPServer(79,Factory_test()).setServiceParent(serviceCollection)
