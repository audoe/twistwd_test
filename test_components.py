from twisted.internet import defer
from twisted.application import service
from twisted.python import components
from twisted.python import log
from twisted.protocols import basic
from twisted.internet import protocol
from twisted.web import resource, xmlrpc, proxy, server, static
class test_resource(resource.Resource):
	def __init__(self, arg):
		super(test_resource, self).__init__()
		self.arg = arg

class inter(components.Interface):
	"""docstring for inter"""
	def getUser(self,user):
		"reutrn the user you want!"
	def getUsers(self):
class test_ds(components.Interface):
		"""docstring for In"""
		def setUsers(self,user,status):
			
def catchError(err):
	return 'return catchError'
class FingerProtocol(basic.LineReceiver):
	"""docstring for FingerProtocol"""
	def LineReceived(self,user):
		d=self.factory.getUser()
		d.addErrback(catchError)
		def writeValue(value):
			self.transport.write(value+'\n')
			self.transport.loseConnection()
		d.addCallback(writeValue)
class IFingerFactory(components.Interface):
	"""docstring for IFingerFactory"""
	def getUser(self,user):
	
	def buildProtocol(self,addr):
	
class FingerFactoryFromService(protocol.ServerFactory):
	"""docstring for FingerFactory"""
	__implements__=IFingerFactory
	protocol=FingerProtocol
	def __init__(self,service):
		self.service=service
	def getUser(self,user):
		return self.service.getUser(user)

components.registerAdapter(FingerFactoryFromService,inter,IFingerFactory)



		
		
				