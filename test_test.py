#_*_coding:utf8_*_
#这是一个使用test的开始
#先写个test
class subClass(object):
	"""这个类其实没什么用的，就是让我使用一些test工具而已"""
	def __init__(self, one,two):
		super(subClass, self).__init__()
		self.one=one
		self.two=two
	def testPrint(self):
		print self.one,self.two
	def testAdd(self):
		return self.one+self.two
	def testDel(self):
		del self.one
		print '删除了one'
        import pdb; pdb.set_trace() ### XXX BREAKPOINT
        print 'fdf'

class subClass(object):
	def __init__(self,x,y):
		self.x=x
		self.y=y
	def testAdd(self):
		print 'dsdsjkhsdjhd'



if __name__ == '__main__':
	test=subClass(23,23)
	print '首先测试一下打印：'
	test.testPrint()
	print '延后测试一下相加：'
	tmp=test.testAdd()
	print '得到的结果是：',tmp
	print '试试删除一个塑性试试:'
    pdb.set_trace()
	test.testDel()
	print '再打印一次：'
	try:
		test.testPrint()
	except Exception, e:
		print '异常了',e.message
	else:
		pass
	finally:
		del test
		print 'test对象删除掉了，这就是传说中的垃圾处理吧！'

