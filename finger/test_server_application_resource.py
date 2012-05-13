from twisted.application import internet ,service   #in the web
from twisted.internet import protocol,reactor,defer
from twisted.protocols import basic
from twisted.web import resource,server,static
import cgi

class FingerProtocol(basic.LineReceiver):    #like Protocol
    def LineReceived(self,user):
        self.factory.getUser(user).addErrback(lambda _:"error")\
                                  .addCallback(lambda m:(\
             self.transport.write(m+"\n\r"),\
             self.transport.loseConnection()))
class MotdResource(resource.Resource):
    def __init__(self,users):
        self.users=users
        resource.Resource.__init__(self)
    def getChild(self,username,request): 
        #this method is about path return back throuth web
        motd=self.users.get(username)  #get the path
        username=cgi.escape(username)  #remove something I don`t know
        if motd is not None:
            motd=cgi.escape(motd)
            text="%s<br>%s"%(username,motd)
        else:
            text="%s<br>no user like this "%username
        return static.Data(text,'text/html')
#write the server
class FingerService(service.Service):
    def __init__(self,filename):
        self.filename=filename
        self._read()
    def _read(self):
        self.users={}
        for line in file(self.filename): #read the file use build id method file()
            user,status=line.split(':',1)
            user=user.strip()
            self.users[user]=status
        self.call=reactor.callLater(10,self._read)  #reread the file in 10 sec
    def getUser(self,user):
        return defer.succeed(self.users.get(user,'no such user'))
    def getFingerFactory(self):
        f=protocol.ServerFactory()
        f.protocol,f.getUser=FingerProtocol,self.getUser
        f.startService=self.startService
        return f
    def getResource(self):
        r=MotdResource(self.users)
        return r
application=service.Application('finger',uid=1,gid=1)
f=FingerService('/etc/users')
serviceCollection=service.IServiceCollection(application)
internet.TCPServer(79,f.getFingerFactory()).setServiceParent(serviceCollection)
internet.TCPServer(8000,server.Site(f.getResource())).setServiceParent(serviceCollection)

