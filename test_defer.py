#_*_coding:utf8_*_
from twisted.application import internet, service
from twisted.internet import protocol, reactor, defer
from twisted.web import resource,server,static
#import pdb; pdb.set_trace() ### XXX BREAKPOINT
from twisted.protocols import basic
class FingerProtocol(basic.LineReceiver):
    #protocol 管理着全部的链接
    def connectionMade(self):
        ti=self.factory.getTime()
        timeString='%d:%d:%d:%d:%d:%d'%(ti.tm_year,ti.tm_mon,ti.tm_mday,ti.tm_hour,ti.tm_min,ti.tm_sec)
   #     import pdb; pdb.set_trace() ### XXX BREAKPOINT
        self.transport.write(timeString)
        self.transport.loseConnection()
class FingerFactory(protocol.ServerFactory):
    protocol=FingerProtocol
    def __init__(self,service):
        self.service=service
    def getTime(self):
        import time
        return time.localtime()

    def getUser(self,user):
        return defer.succeed(self.users.get(user,'No such user'))
class FingerTrue(basic.LineReceiver):
    def __init__(self):
        self.now=0
        self.name=''
    def connectionMade(self):
        self.transport.write('place inter you name first:')
    def lineReceived(self,String):
        if self.now==0:
            self.name=String
            tmp=self.factory.getNews()
            strA='\n'.join(tmp[0])
            self.transport.write(strA+'\n')
            self.now=tmp[1]
        elif String!='':
            newTmp=self.name+' '+String+' '+self.factory.getTime()
            self.factory.setNews(newTmp)
            tmp=self.factory.getNews(self.now)
            self.transport.write('\n'.join(tmp[0])+'\n')
            self.now=tmp[1]
        else:
            tmp=self.factory.getNews(self.now)
            self.transport.write('\n'.join(tmp[0])+'\n')
            self.now=tmp[1]
class webT(resource.Resource):
    __implements__=resource.IResource
    def __init__(self,service):
        resource.Resource.__init__(self)
        self.service=service
        self.putChild('',self)
        self.putChild('check',webUser(self.service))
    def render_GET(self,request):
        ti=self.service.getTime()
        fi=open('/home/whchen/tem.html','r')
        t=fi.read()
        fi.close()
        return t%ti
    def getChild(self,path,request):
        if path=='user':
            return webUser()
        if path=='favicon.ico':
            return static.File('/home/whchen/logo.jpg')
        if path=='index.css':
            return static.File('/home/whchen/index.css')
        if path=='getoff':
            return static.File('/home/whchen/client.py')

class webUser(resource.Resource):
    __implements__=resource.IResource
    def __init__(self,service):
        resource.Resource.__init__(self)
        self.service=service
        self.putChild('uid',webUid())
    def render_GET(self,request):
        return self.service.getTime()
class webUid(resource.Resource):
    def render_GET(self,request):
        return 'dsd'
class FingerFactory_one(protocol.ServerFactory):
    protocol=FingerTrue
    def __init__(self,service):
        self.service=service
    def getNews(self,now=0):
        return self.service.getNews(now)
    def setNews(self,Strings):
        self.service.setNews(Strings)
    def getTime(self):
        return self.service.getTime()
class serviceTmp(service.Service):
    def __init__(self, fileName):
        self.file = open(fileName, 'r')
        self.news = self.file.read().split('\n')
        self.file.close()
        self.count = 0
        self.file=open(fileName, 'a')
    def setNews(self,Strings):
        self.news.append(Strings)
        self.file.write(Strings+'\n')
    def getTime(self):
        import time
        tmp_Time=time.localtime()
        tmp_Str='%d:%d:%d'%(tmp_Time.tm_hour,tmp_Time.tm_min,tmp_Time.tm_sec)
        return tmp_Str
    def getNews(self,num=0):
        if num==0:
            return (self.news[-10:],len(self.news))
        else:
            return (self.news[num:],len(self.news))
application=service.Application('finger',uid=1,gid=1)
serviceOne=serviceTmp('tmpfile')
factory=FingerFactory(serviceOne)
factory_one=FingerFactory_one(serviceOne)
internet.TCPServer(79,factory).setServiceParent(service.IServiceCollection(application))
internet.TCPServer(89,factory_one).setServiceParent(service.IServiceCollection(application))
webOne=webT(serviceOne)
internet.TCPServer(80,server.Site(webOne)).setServiceParent(service.IServiceCollection(application))
