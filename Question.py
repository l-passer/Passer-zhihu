#encoding=utf8
import requests,Util,threading,queue,urllib,ThreadUtil

class Question(object):

	def __init__(self,question_id,cookies):
		self.s = requests.session()
		cookieJar = requests.utils.cookiejar_from_dict(cookies)
		self.s.cookies = cookieJar
		self.question_id = question_id
		self.url_queue = queue.Queue()
		self.html_queue = queue.Queue()

	def archieve_answerlist(self,ftype = 'answers',thread_number = 10):
		
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
					answer_content = x['excerpt']
					answer_createtime = x['created_time']
					answer_updatetime = x['updated_time']
					answer_votecount = x['voteup_count']
					answer_commentnum = x['comment_count']
					author_name = x['author']['name']
					author_id = x['author']['url_token']
					author_gender = x['author']['gender']
					author_headline = x['author']['gender']

					print(author_name,author_gender,answer_votecount,answer_commentnum,author_headline,answer_content)

				self.html_queue.task_done()