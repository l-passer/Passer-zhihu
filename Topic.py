#encoding=utf8
import requests,Util,threading,queue,urllib,ThreadUtil,re
from bs4 import BeautifulSoup
from Save import *

class Topic(object):

	def __init__(self,topicid,cookies):
		self.topicid = topicid
		self.s = requests.session()
		cookieJar = requests.utils.cookiejar_from_dict(cookies)
		self.s.cookies = cookieJar

	def init_common(self,itype):
		''' 精华问题：top-answers
			所有问题：questions
		'''
		r = self.s.get(url = '{}{}/{}'.format(Util.TOPIC_API,self.topicid,itype),headers = Util.Default_Headers)
		print('{}{}/{}'.format(Util.TOPIC_API,self.topicid,itype),r.status_code)
		if r.status_code == 200:
			pagelist = re.findall(r'(?<=\?page=)[0-9]{1,}(?=">)',r.text)
			if len(pagelist) > 2:
				countPage = int(pagelist[-2])
			else:
				countPage = 1
		
		for page in range(1,countPage+1):
			self.url_queue.put('{}{}/{}?page={}'.format(Util.TOPIC_API,self.topicid,itype,page))

	def archieve_list(self,thread_number=10,itype='questions'):
		self.url_queue = queue.Queue()
		self.html_queue = queue.Queue()
		self.result_queue = queue.Queue()
		self.init_common(itype)
		self.url_queue.put(Util.ENG_FLAG)

		for x in range(0,thread_number):
			thread = threading.Thread(target=ThreadUtil.thread_queue,args=(self.url_queue,self.html_queue,self.s,))
			thread.start()

		for x in range(0,thread_number):
			thread = threading.Thread(target=self.parse_common,args=(itype,))
			thread.start()

	def save_thread(self):
		while True:
			if not self.result_queue.empty():
				result = self.result_queue.get()
				if result == Util.ENG_FLAG:
					break
				self.save.write_excle(result)

	def save_list(self,xlsfile,thread_number=10):
		self.save = Save_Excle()
		tlist = []
		for x in range(0,thread_number):
			thread = threading.Thread(target=self.save_thread)
			thread.start()
			tlist.append(thread)

		for x in tlist:
			x.join()

		self.save.store_excle(xlsfile)

	def parse_common(self,itype):
		while True:
			if not self.html_queue.empty():
				html_page = self.html_queue.get()
				if html_page == Util.ENG_FLAG:
					self.result_queue.put(Util.ENG_FLAG)
					break

				b = BeautifulSoup(html_page.text,'lxml')
				if itype == 'questions':
					items = b.find_all('div',{'itemprop':'question'})
					for item in items:
						question_time = item.find('span',{'class':'time'})['data-timestamp']
						question_info = item.find('a',{'class':'question_link'})
						question_href = question_info['href']
						question_title = question_info.text
						print(question_time,question_href,question_title)
						self.result_queue.put([question_time,question_href,question_title])

				elif itype == 'top-answers':
					items = b.find_all('div',{'class':'feed-main'})
					for item in items:
						question = item.find('a',{'class':'question_link'})
						question_url = question['href']
						question_title = question.text

						answer_href = item.find('link',{'itemprop':'url','href':re.compile(r'/question/[0-9]{1,}/answer/[0-9]{1,}')})
						answer_href = answer_href['href'] if answer_href else None

						vote_number = item.find('a',class_='zm-item-vote-count js-expand js-vote-count')
						vote_number = vote_number.text if vote_number else 0

						author = item.find('a',{'class':'author-link'})
						author_name,author_href = None,None
						if author:
							author_name = author.text
							author_href = author['href']

						item_time = item.find('a',class_='answer-date-link meta-item')
						create_time,modify_time = None,None
						if item_time:
							try:
								create_time = item_time['data-tooltip']
							except Exception as e:
								pass
							modify_time = item_time.text

						print(question_url,question_title,answer_href,vote_number,author_name,author_href,create_time,modify_time)
						self.result_queue.put([question_url,question_title,answer_href,vote_number,author_name,author_href,create_time,modify_time])