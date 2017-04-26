import time

Default_Headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36',
            'Host': 'www.zhihu.com'}
COOKIE = ''

BASE_URL = 'https://www.zhihu.com'

PHONE_LOGIN = BASE_URL + '/login/phone_num'
CAPTCHA_URL = BASE_URL+'/captcha.gif?r='+str(int(time.time())*1000)+'&type=login'

QUESTION_API = BASE_URL + '/api/v4/questions'
ANSWER_API = BASE_URL + '/api/v4/answers'

PERSOINFO_API = BASE_URL + '/people/'
MEMBER_API = BASE_URL + '/api/v4/members'

TOPIC_API = BASE_URL + '/topic/'

ENG_FLAG = 'End'