#encoding=utf8
import requests,Util,threading,queue,urllib,ThreadUtil,re
from bs4 import BeautifulSoup

class Topic(object):

	def __init__(self,topicid,cookies):
		self.topicid = topicid
		self.s = requests.session()
		cookieJar = requests.utils.cookiejar_from_dict(cookies)
		self.s.cookies = cookieJar

	def archieve_topanswers(self,thread_number=10):
		self.url_queue = queue.Queue()
		self.html_queue = queue.Queue()
		self.init_topanswers()
		self.url_queue.put(Util.ENG_FLAG)

		for x in range(0,thread_number):
			thread = threading.Thread(target=ThreadUtil.thread_queue,args=(self.url_queue,self.html_queue,self.s,))
			thread.start()

		for x in range(0,thread_number):
			thread = threading.Thread(target=self.parse_topanswers)
			thread.start()


	def init_topanswers(self):
		r = self.s.get(url = '{}{}/top-answers'.format(Util.TOPIC_API,self.topicid),headers = Util.Default_Headers)
		if r.status_code == 200:
			pagelist = re.findall(r'(?<=\?page=)[0-9]{1,}(?=">)',r.text)
			if len(pagelist) > 2:
				countPage = int(pagelist[-2])
			else:
				countPage = 1
		
		for page in range(1,countPage+1):
			print('{}{}/top-answers?page={}'.format(Util.TOPIC_API,self.topicid,page))
			self.url_queue.put('{}{}/top-answers?page={}'.format(Util.TOPIC_API,self.topicid,page))

	def parse_topanswers(self):
		while True:
			if not self.html_queue.empty():
				html_page = self.html_queue.get()
				if html_page == Util.ENG_FLAG:
					break

				b = BeautifulSoup(html_page.text,'lxml')
				items = b.find_all('div',{'class':'feed-main'})
				for item in items:
					question = item.find('a',{'class':'question_link'})
					question_url = question['href']
					question_title = question.text

					answer_href = item.find('link',{'itemprop':'url','href':re.compile(r'/question/[0-9]{1,}/answer/[0-9]{1,}')})
					answer_href = answer_href['href'] if answer_href else None

					vote_number = item.find('a',class_='zm-item-vote-count js-expand js-vote-count')
					vote_number = vote_number.text if vote_number else 0

					answer_content = item.find('textarea',{'class':'content'})
					answer_content = answer_content.text if answer_content else None

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


					print(question_url,question_title,answer_href,vote_number,author_name,author_href,create_time,modify_time,answer_content)