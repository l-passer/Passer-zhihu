#encoding=utf8
import time,requests,re,pickle,os,queue,urllib,threading,ThreadUtil
from PIL import Image
from bs4 import BeautifulSoup
import Util

class User(object):

	def __init__(self):
		self.s = requests.session()

	def login(self,username,password):

		usercookies = {}

		if os.path.isfile('usercookie/{}.text'.format(username)):
			with open('usercookie/{}.text'.format(username),'rb') as f:
				usercookies = pickle.load(f)
			return usercookies

		catpcha_image = self.archieve_captcha()
		catpcha = input('please input captcha...')

		data = {"phone_num":username,"password":password,"captcha":catpcha}
		status = self.s.post(Util.PHONE_LOGIN,headers = Util.Default_Headers,data= data)
		print(status.json()['msg'])

		if status.status_code == 200:		
			usercookies = requests.utils.dict_from_cookiejar(self.s.cookies)
			with open('usercookie/{}.text'.format(username),'wb') as f:
				pickle.dump(usercookies,f)
		else:
			pass

		return usercookies

	def archieve_captcha(self):
		c = self.s.get(Util.CAPTCHA_URL,headers=Util.Default_Headers)
		print(Util.CAPTCHA_URL)
		if c.status_code == 200:
			with open('capture.gif','wb') as f:
				f.write(c.content)
			image = Image.open('{}/capture.gif'.format(os.getcwd()))
			image.show()
		else:
			return 'archieve capture fail.'

	def isValid(self):
		cookieJar = requests.utils.cookiejar_from_dict(Util.COOKIE)
		self.s.cookies = cookieJar
		if self._find_xsrf():
			return True
		else:
			return False

	def archieve_xsrf(self):
		cookieJar = requests.utils.cookiejar_from_dict(Util.COOKIE)
		self.s.cookies = cookieJar
		res = self._find_xsrf()
		if res:
			return res['value']
		else:
			return 'user not valid.'

	def _find_xsrf(self):
		c = BeautifulSoup(self.s.get(Util.BASE_URL,headers=Util.Default_Headers).content,'lxml')
		xsrf = c.find('input',{'name':'_xsrf'})
		return xsrf

	def archieve_userinfo(self,userid):
		print('{}{}/answers'.format(Util.PERSOINFO_API,userid))
		r = self.s.get(url = '{}{}/answers'.format(Util.PERSOINFO_API,userid),headers=Util.Default_Headers)
		if r.status_code == 200:

			b = BeautifulSoup(r.content,'lxml')

			user_name = b.find('span',{'class':'ProfileHeader-name'})
			user_name = user_name.text if user_name else None

			user_headline = b.find('span',class_='RichText ProfileHeader-headline')
			user_headline = user_headline.text if user_headline else None

			user_company = b.find('svg',class_='Icon Icon--company')
			if user_company:
				user_company = user_company.parent.parent.text
			else:
				user_company = None

			user_education = b.find('svg',class_='Icon Icon--education')
			if user_education:
				user_education = user_education.parent.parent.text
			else:
				user_education = None

			user_follow = b.find_all('div',{'class':'NumberBoard-value'})
			user_follower,user_followee = -1,-1
			if len(user_follow) == 2:
				user_follower,user_followee = user_follow[0].text,user_follow[1].text

			user_otherinfo = b.find_all('span',{'class':'Profile-lightItemValue'})
			takein_live,followe_topic,followe_zhuanlan,followe_question,followe_collection = 0,0,0,0,0
			if len(user_otherinfo) == 5:
				takein_live = user_otherinfo[0].text
				followe_topic = user_otherinfo[1].text
				followe_zhuanlan = user_otherinfo[2].text
				followe_question = user_otherinfo[3].text
				followe_collection = user_otherinfo[4].text

			user_activity = b.find_all('span',{'class':'Tabs-meta'})
			answer_num,share_num,question_num,collection_num = 0,0,0,0
			if len(user_activity) == 4:
				answer_num = user_activity[0].text
				share_num = user_activity[1].text
				question_num = user_activity[2].text
				collection_num = user_activity[3].text

			re_votenumber = r'(?<=获得 )[0-9]{1,}(?= 次赞同)'
			re_thanknumber = r'(?<=获得 )[0-9]{1,}(?= 次感谢)'
			re_collectnumber = r'(?<=，)[0-9]{1,}(?= 次收藏)'
			re_includenumber = r'(?<=收录 )[0-9]{1,}(?= 个回答)'

			c = r.text
			f = lambda x:x.group() if x else 0
			votenumber = f(re.search(re_votenumber,c))
			thanknumber = f(re.search(re_thanknumber,c))
			collectnumber = f(re.search(re_collectnumber,c))
			includenumber = f(re.search(re_includenumber,c))

			print(user_name,user_headline,user_company,user_education,user_follower,user_followee,
				takein_live,followe_topic,followe_zhuanlan,followe_question,followe_collection,
				answer_num,share_num,question_num,collection_num,votenumber,thanknumber,collectnumber,includenumber)
		else:
			print('archieve userinfo fail,please retry.')
			return None

	def archieve_list(self, userid, ftype = 'followers', thread_number = 10):
		self.url_queue = queue.Queue()
		self.html_queue = queue.Queue()
		self.init_followee_url(userid,ftype)
		self.url_queue.put(Util.ENG_FLAG)

		for x in range(thread_number):
			thread = threading.Thread(target=ThreadUtil.thread_queue,args=(self.url_queue,self.html_queue,self.s,))
			thread.start()

		for x in range(thread_number):
			thread = threading.Thread(target=self.parser_followelist_page_thread,args=(ftype,))
			thread.start()

	def init_followee_url(self,userid,ftype):

		url = Util.MEMBER_API + '/' + userid + '/' + ftype
		ThreadUtil.init_thread(url,20,self.url_queue,self.s)


	def parser_followelist_page_thread(self,ftype):
		while True:
			if not self.html_queue.empty():
				html_page = self.html_queue.get()
				if html_page == Util.ENG_FLAG:
					break

				if ftype == 'followees' or ftype == 'followers':	
					html_page = html_page.json()
					for x in html_page['data']:
						answer_count = x['answer_count']
						articles_count = x['articles_count']
						gender = x['gender']
						name = x['name']
						url_token = x['url_token']
						follower_count = x['follower_count']
						if int(follower_count) < 1000 and int(follower_count) > 100:
							print(url_token)

					self.html_queue.task_done()
				
				elif ftype == 'following-columns':
					html_page = html_page.json()
					for x in html_page['data']:
						title = x['title']
						articles_count = x['articles_count']
						followers = x['followers']
						updated = x['updated']
						column = x['id']
						intro = x['intro']
						print(title,articles_count,followers,updated,column,intro)

				elif ftype == 'following-questions' or ftype == 'questions':
					html_page = html_page.json()
					for x in html_page['data']:
						title = x['title']
						url = x['url']
						updated_time = x['updated_time']
						answer_count = x['answer_count']
						follower_count = x['follower_count']
						created  =x['created']
						print(title,url,updated_time,answer_count,follower_count,created)