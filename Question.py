#encoding=utf8
import requests,Util,threading,queue,urllib,ThreadUtil
import csv,codecs,re
from bs4 import BeautifulSoup

class Question(object):

	def __init__(self,question_id,cookies):
		self.s = requests.session()
		cookieJar = requests.utils.cookiejar_from_dict(cookies)
		self.s.cookies = cookieJar
		self.question_id = question_id
		self.url_queue = queue.Queue()
		self.html_queue = queue.Queue()

	def archieve_question_info(self):
		r = self.s.get(url='{}{}'.format(Util.QUESTION_URL,self.question_id),headers=Util.Default_Headers)
		if r.status_code == 200:
			b = BeautifulSoup(r.content,'lxml')
			scanlist = b.find_all('div',{'class':'NumberBoard-value'})
			scantimes,followers = 0,0
			if scanlist:
				scantimes = scanlist[0].text
				followers = scanlist[1].text

			rex = r'(?<=<span>)[0-9]{1,}(?= 个回答</span>)'
			answer_count = re.findall(rex,r.text)[0]

			return scantimes,followers,answer_count
		return 0,0,0

	def archieve_answerlist(self,ftype = 'answers',thread_number = 1):
		
		self.init_answerlist_url(ftype)
		self.url_queue.put(Util.ENG_FLAG)

		for x in range(thread_number):
			thread = threading.Thread(target=ThreadUtil.thread_queue,args=(self.url_queue,self.html_queue,self.s,))
			thread.start()

		for x in range(thread_number):
			thread = threading.Thread(target=self.parser_answerlist_page_thread)
			thread.start()

	def init_answerlist_url(self,ftype):

		url = Util.QUESTION_API + '/' + self.question_id + '/' + ftype
		ThreadUtil.init_thread(url,20,self.url_queue,self.s)

	def parser_answerlist_page_thread(self):
		while True:
			if not self.html_queue.empty():
				html_page = self.html_queue.get()
				if html_page == Util.ENG_FLAG:
					break
					
				html_page = html_page.json()
				for x in html_page['data']:
					answer_content = x['content']
					answer_excerpt = x['excerpt']
					answer_createtime = x['created_time']
					answer_updatetime = x['updated_time']
					answer_votecount = x['voteup_count']
					answer_commentnum = x['comment_count']
					author_name = x['author']['name']
					author_id = x['author']['url_token']
					author_gender = x['author']['gender']
					author_headline = x['author']['headline']
					
					answer_content,n = re.subn(Util.HTML_TAG_REX,'',answer_content)
					print(answer_createtime,answer_votecount,answer_commentnum,author_gender,answer_content)

				self.html_queue.task_done()