#_*_coding:utf8_*_
from  twisted.internet.protocol import Protocol,ClientFactory
from time import sleep
from os import popen


class CheckTheTime(Protocol):
    def __init__(self):
        self.i=0
    def dataReceived(self,data):
        date,time=data.split('-')
        if self.i==0:
           print '欢迎你，第一次连接'
        print date,time
        print self.i
        self.i+=1
class TimeFactory(ClientFactory):
    def startedConnecting(self,connector):
        print 'connection'
    def buildProtocol(self,addr):
        return CheckTheTime()
    def clientConnectionFailed(self,connector,reason):
        print 'connectFailed'
        reactor.stop()
from twisted.internet import reactor
if __name__=='__main__':
    try:
        ip=open('ip.txt','r').read()
    except:
        ip='localhost'
    from optparse import OptionParser
    parser=OptionParser()
    parser.add_option('-a','--host',default=ip,dest='host',help='the server host of you want to connect',metavar='HOST')
    parser.add_option('-p','--port',default='79',dest='port',help='server port',metavar='PORT')
    (options,args)=parser.parse_args()
    host=options.host
    port=int(options.port)
    reactor.connectTCP(host,port,TimeFactory())
    reactor.run()
