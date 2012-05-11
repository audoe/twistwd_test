from twisted.internet import pollreactor
pollreactor.install()
from twisted.internet import reactor
import traceback
def hello():
    print 'dsadsdsd'
    traceback.print_stack()
reactor.callWhenRunning(hello)
reactor.run()
