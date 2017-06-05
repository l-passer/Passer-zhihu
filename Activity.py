#encoding=utf8
import urllib,Util
from IpProxy import *

class Activity(object):

	def __init__(self):
		self.s = requests.session()
		self.proxies = {}
		self.proxies['https'] = Proxy().archieve_activity_proxy()
		
	def archieve_activities(self,userid,limit):

		post_data = {'after_id':1493717719,'limit':limit,'desktop':True}
		data = urllib.parse.urlencode(post_data)
		url = Util.MEMBER_API + '/' + userid + '/activities'

		while True:
			try:
				html_page = self.s.get(url='{}?{}'.format(url,data),headers=Util.Default_Headers,proxies = self.proxies)
				code = html_page.status_code
				if code == 200:
					j = html_page.json()
					for x in j['data']:
						created_time = x['created_time']
						verb = x['verb']
						print(created_time,verb)
					
				break
			except Exception as e:
				self.proxies['https'] = Proxy().archieve_activity_proxy()
		