#_*_coding:utf8_*_
from twisted.application import internet,service
from twisted.internet import protocol,reactor,defer
from twisted.protocols import basic
class FingerProtocol(basic.LineReceiver):
    #protocol 管理着全部的链接
	def lineReceived(self,user):
		self.factory.getUser(user).addErrback(lambda _:"error").addCallback(lambda m:(self.transport.write(m+"\r\n"),self.transport.loseConnection()))
class FingerFactory(protocol.ServerFactory):
	"""docstring for FingerFactory"""
	protocol=FingerProtocol
	def __init__(self, **kword):
		self.users=kword
	def getUser(self,user):
		return defer.succeed(self.users.get(user,'No such user'))
application=service.Application('finger',uid=1,gid=1)
factory=FingerFactory(audoe='dsdsdsds')
internet.TCPServer(79,factory).setServiceParent(service.IServiceCollection(application))

    
    
