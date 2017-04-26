#encoding=utf8
import requests,Util,threading,queue,re,urllib,ThreadUtil
from bs4 import BeautifulSoup
import Util


class Answer(object):

	def __init__(self,answer_url,cookies):
		self.answer_url = answer_url
		self.answer_id = answer_url.split('/')[-1]
		self.s = requests.session()
		cookieJar = requests.utils.cookiejar_from_dict(cookies)
		self.s.cookies = cookieJar
		self.html_queue = queue.Queue()
		self.url_queue = queue.Queue()

	def archieve_answer_detail(self):
		r = self.s.get(self.answer_url,headers=Util.Default_Headers)
		if r.status_code == 200:
						
			b = BeautifulSoup(r.content,'lxml')
			author_info = b.find('span',class_='UserLink AuthorInfo-avatarWrapper')
			author_link = author_info.find('a',{'class':'UserLink-link'})

			if author_link:
				author_href = Util.BASE_URL + author_link['href']
				author_name = author_link.find('img')['alt']
			else:
				author_href = None
				author_name = None

			answer_content = b.find('span',class_='RichText CopyrightRichText-richText')
			if answer_content:
				answer_content = answer_content.text
			else:
				answer_content = None

			c = r.text
			answer_voteup = re.search(r'(?<=button">)[0-9]{1,}(?= 人赞同了该回答)',c).group()
			if not answer_voteup:
				answer_voteup = -1

			answer_comment = re.search(r'(?<=</svg>)[0-9]{1,}(?= 条评论)',c).group()
			if not answer_comment:
				answer_comment = -1

			answer_favnumber = self.archieve_answer_favtimes()

			print(author_href,author_name,answer_voteup,answer_comment,answer_favnumber)
			return author_href
		else:
			print('fail')
			return None

	def archieve_answer_favtimes(self):
		post_data = {'offset':0,'limit':10}
		data = urllib.parse.urlencode(post_data)
		rj = self.s.get(url = '{}/{}/favlists?{}'.format(Util.ANSWER_API,self.answer_id,data),headers = Util.Default_Headers)
		print(rj.status_code)
		if rj.status_code == 200:
			answer_favnumber = rj.json()['paging']['totals']
		else:
			answer_favnumber = -1
		return answer_favnumber

	def archieve_answer_list(self,ftype ='favlists',threadNumber = 10):
		self.init_list_url(ftype)
		self.url_queue.put(Util.ENG_FLAG)

		for x in range(0,threadNumber):
			thread = threading.Thread(target=ThreadUtil.thread_queue,args=(self.url_queue,self.html_queue,self.s,))
			thread.start()

		for x in range(0,threadNumber):
			thread = threading.Thread(target=self.parse_answer_favlist,args=(ftype,))
			thread.start()

	def init_list_url(self,ftype):
		url = Util.ANSWER_API + '/' + self.answer_id + '/' + ftype
		ThreadUtil.init_thread(url,10,self.url_queue,self.s)

	def parse_answer_favlist(self,ftype):
		while True:
			if not self.html_queue.empty():
				html_page = self.html_queue.get()
				if html_page == Util.ENG_FLAG:
					break

				html_page = html_page.json()
				if ftype == 'favlists':
					for x in html_page['data']:
						collect_id = x['id']
						collect_title = x['title']
						collect_updatetime = x['updated_time']
						collect_count = x['answer_count']
						creator_name = x['creator']['name']
						creator_token = x['creator']['url_token']
						creator_gender = x['creator']['gender']
						creator_headline = x['creator']['headline']
						print(collect_id,collect_title,collect_updatetime,collect_count,creator_name)

				elif ftype == 'voters':
					for x in html_page['data']:
						name = x['name']
						url_token = x['url_token']
						gender = x['gender']
						answer_count = x['answer_count']
						articles_count = x['articles_count']
						follower_count = x['follower_count']
						print(name,url_token,gender,answer_count,articles_count,follower_count)