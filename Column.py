#encoding=utf8
import requests,Util,threading,queue,urllib,ThreadUtil

class Column(object):

	def __init__(self,columnid,cookies):
		self.s = requests.session()
		cookieJar = requests.utils.cookiejar_from_dict(cookies)
		self.s.cookies = cookieJar
		self.columnid = columnid

	def zhuanlan_info(self):
		pass

	def archieve_articles(self):
		url = Util.ZHUANLAN_ARTICLE +  '/' + self.columnid + '/posts'
		offset,pageCount = 0,20
		post_data = {'offset':offset,'limit':pageCount}
		Util.Default_Headers['Host'] = 'zhuanlan.zhihu.com'
		
		while True:
			post_data['offset'] = offset*pageCount + 1
			data = urllib.parse.urlencode(post_data)
			r = self.s.get('{}?{}'.format(url,data),headers=Util.Default_Headers)
			html_page = r.json()
			if html_page:
				self.parse_article(html_page)
				offset += 1
			else:
				break


	def parse_article(self,html_page):		
		for x in html_page:
			title = x['title']
			url = x['url']
			titleImage = x['titleImage']
			publishedTime  =x['publishedTime']
			likesCount = x['likesCount']
			commentsCount = x['commentsCount']
			content = x['content']
			author_name = x['author']['name']
			author_slug = x['author']['slug']
			print(title,url,titleImage,publishedTime,likesCount,commentsCount,content,author_name,author_slug)