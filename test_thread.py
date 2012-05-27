#_*_coding:utf8_*_
from threading import Thread
from Queue import Queue
from lxml.html import soupparser, tostring, parse
import re
import urllib 
class Threadpool(object):
	"""pool thread 
	"""
	def __init__(self, thread_num=0,deep=2,key_word='',site=''):
		self.thread_num = thread_num
		self.deep = deep
		self._queue=Queue()
		self.thread_list=[]
		self.view=[]
		self.key_word=key_word
		self.site=re.compile(site)
		self._build_thread(thread_num)
		self._active_thread()
		
	
	def _build_thread(self,thread_num):
		for i in range(thread_num):
			Work(self._queue,self.key_word,self.deep,self.site,self.view)
	def add_job(self,url):
		html=parse(url).getroot()
		li=html.xpath('//a[@href]/@href')
		for i in li:
			if self.site.findall(i):
				self._queue.put(i)
			else:
				pass
	def _active_thread(self):
		for i in self.thread_list:
			if i.isAlive():
				i.join()
class Work(Thread):
	"""this is thread of dig web page where deep is some num"""
	def __init__(self, queue,key_word,deep,site,view):
		Thread.__init__(self)
		self.key_word=key_word
		self.deep=deep
		self.queue = queue
		self.deep_check=re.compile('(\/)')
		self.site=site
		self.host=re.compile(r'//(.*?[^/])(/|$)')
		self.start()
		self.view=view
		self.ispath=re.compile('\?')
	def run(self):
		while True:
			tmp=self.queue.get()
			print tmp
			tmp_host=self.host.findall(tmp)[0][0]
			try:
				tmp_file=urllib.urlopen(tmp).read()
				tes=soupparser.fromstring(tmp_file)
			except:
				continue

			tmp_file=tostring(tes,encoding='utf8')
			url_list=tes.xpath('//a[@href]/@href')
			self.del_url(url_list,self.deep,tmp_host)
			self.save_page(tmp,tmp_file)
			self.queue.task_done()
	def save_page(self,html,str):
		url=html
		self.view.append(url)
		tmp=url.split('?')[0].split('//')[1]
		file_tmp=''
		file_path=tmp.replace('.','/')
		if file_path.endswith('/'):
			file_path=file_path+'index.html'
		file_tmp=file_path.replace('/','_')
		print file_tmp
		if file_tmp is '':
			file_tmp='dssd'
		tmp_file=open('file/'+file_tmp,'w')
		tmp_file.write(str)
		tmp_file.close()
	def del_url(self,url_list,deep,tmp_host):
		for i in url_list:
			if 	i.startswith('http'):
				# 绝对地址
				if len(self.deep_check.findall(i))>deep+2:
					pass
				else:
					if self.site.findall(tmp_host):
						if self.ispath.findall(i):
							pass
						elif i in self.view:
							pass
						else:
							self.queue.put(i)
					else:
						pass
			else:
				pass



if __name__ == '__main__':
	pool_num=5
	deep=2
	site='sina.com.cn'
	pool=Threadpool(pool_num,deep,'dsfs',site)
	pool._build_thread(pool_num)
	pool.add_job('http://www.sina.com.cn')
	pool._active_thread()
	from time import sleep

	while True:
		sleep(10)
		print pool._queue.qsize(),len(pool.view)
		