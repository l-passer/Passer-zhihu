import requests,time
class Proxy:

	'''
		获取代理。
		需要的参数：需要代理的数量,需要http还是https类型的代理
		返回代理的列表

		achieve_proxy:限定http或者https

	'''
	def __init__(self):
		self.ip_url = 'http://api.ip.data5u.com/api/get.shtml?order=2c08b1c0a1744f727c8970930b5fa29b&num=1&area=%E4%B8%AD%E5%9B%BD&carrier=0&protocol=0&an1=1&an2=2&an3=3&sp1=1&sp2=2&sp3=3&sort=1&system=1&distinct=0&rettype=0&seprator=%0D%0A'
		self.proxylist = []

	def achieve_proxy_http(self,proxy_num,proxy_type):

		proxy_list = []

		for i in range(proxy_num):
			ipjson = requests.get(self.ip_url,timeout=2).json()
			if ipjson['data'] and ipinfo['type'] == proxy_type:
				ipinfo = ipjson['data'][0]
				proxies = '"{}":"{}://{}:{}"'.format(proxy_type,proxy_type,ipinfo['ip'],ipinfo['port'])
				if self.test_proxy(proxies):
					print('可用 -- {}'.format(proxies))
					proxy_list.append(proxies)
				else:
					print('不可用 -- {}'.format(proxies))

		return proxy_list


	def achieve_proxy(self,proxy_num):
		proxy_list = []

		while len(proxy_list) < proxy_num:
			try:
				ipjson = requests.get(self.ip_url,timeout=2).json()
				if ipjson['data']:
					proxies = {}
					ipinfo = ipjson['data'][0]
					proxies[ipinfo['type']] = '{}://{}:{}'.format(ipinfo['type'],ipinfo['ip'],ipinfo['port'])
					if self.test_proxy(proxies):
						proxy_list.append(proxies)
					else:
						pass
				time.sleep(1)
			except Exception as e:
				pass

		return proxy_list

	def test_proxy(self,proxies):
		test_url = 'http://1212.ip138.com/ic.asp'
		try:
			r = requests.get(url = test_url,proxies=proxies,timeout = 1)
		except Exception as e:
			return False

		if requests.get(url = test_url,proxies=proxies).status_code == 200:
			return True
		else:
			return False

	def archieve_pool(self):
		if len(self.proxylist) < 6:
			url = 'http://api.ip.data5u.com/api/get.shtml?order=2c08b1c0a1744f727c8970930b5fa29b&num=50&carrier=0&protocol=2&an1=1&an2=2&an3=3&sp1=1&sp2=2&sp3=3&sort=1&system=1&distinct=0&rettype=1&seprator=%0D%0A'
			r = requests.get(url=url).text
			self.proxylist = r.split('\r\n')[:-2]

		x = self.proxylist[-1]
		self.proxylist.pop()
		return 'https://{}'.format(x)

	def archieve_activity_proxy(self):
		url = 'http://api.ip.data5u.com/dynamic/get.html?order=2c08b1c0a1744f727c8970930b5fa29b'
		r = requests.get(url=url).text.strip()
		return 'https://{}'.format(r)