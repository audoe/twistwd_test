from twisted.protocols.base.portforword import ProxyFactory
from twisted.application import internet,service
class test(ProxyFactory):
    def __init__(self):
        self.port=3000
        self.host='192.168.0.102'
application=service.Application('proxy',uid=1,gid=1)
serviceCollection=service.IServiceCollection(application)
internet.TCPServer(3001,test()).setServiceParent(service)

