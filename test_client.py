#_*_coding:utf8_*_
from  twisted.internet.protocol import Protocol,ClientFactory
from time import sleep
from os import popen


#protocol 协议
#作用是将服务器上的时间设置在客户端上
class CheckTheTime(Protocol):
    def dataReceived(self,data):
        print data
        print 'test first'
#factory 生成连接，并在一定时间后从连
class TimeFactory(ClientFactory):
    def startedConnecting(self,connector):
        print 'connection'
    def buildProtocol(self,addr):
        return CheckTheTime()
    def clientConnectionLost(self,connector,reason):
        print 'connection lost the reason is:'%reason
        #after 10 sec reconnet
        sleep(10)
        connector.connect()
from twisted.internet import reactor
if __name__=='__main__':
    from optparse import OptionParser
    parser=OptionParser()
    parser.add_option('-a','--host',default='localhost',dest='host',help='the server host of you want to connect',metavar='HOST')
    parser.add_option('-p','--port',default='79',dest='port',help='server port',metavar='PORT')
    (options,args)=parser.parse_args()
    host=options.host
    port=int(options.port)
    reactor.connectTCP(host,port,TimeFactory())
    reactor.run()
