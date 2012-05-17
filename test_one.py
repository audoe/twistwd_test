from twisted.application import internet, service, strports
from twisted.internet import protocol, reactor, defer
from twisted.protocols import basic, irc
from twisted.python import components
from twisted.web import resource, server, static, xmlrpc, microdom
from twisted.web.woven import page, model, interfaces
from twisted.spread import pb
from OpenSSL import SSL
import cgi
class IFingerService(components.Interface):
	"""docstring for IFingerService"""
	def getUser(self,user):
	
	def getUsers(self):
		
class IFingerSetterService(components.Interface):
	"""docstring for IFingerSetterService"""
	def setUser(self,user,status):

def catchError(err):
	return 'something is wrong'
class FingerProtocol(basic.LineReceiver):
	"""docstring for FingerProtocol"""
	def lineReceived(self,user):
		d=self.factory.getUser(user)
		d.addErrback(catchError)
		def writeValue(value):
			self.transport.write(value+'\n')
			self.transport.loseConnection()
		d.addCallback(writeValue)
class IFinferFactory(components.Interface):
	"""docstring for IFinferFactory"""
	def getUser(self,user):
	
	def buildProtocol(self,addr):


class FingerFactoryFromService(protocol.ServerFactory):
	"""docstring for FingerFactoryFromService"""
	__implements__=protocol.ServerFactory.__implements__,IFinferFactory
	protocol=FingerProtocol
	def __init__(self,service):
		self.service=service
	def getUser(self,user):
		return self.service.getUser(user)
components.registerAdapter(FingerFactoryFromService,IFingerService,IFinferFactory)


class FingerSetterProtocol(basic.LineReceiver):
	"""docstring for FingerSetterProtocol"""
	def connectionMade(self):
		self.line=[]
	def ():
		pass


		