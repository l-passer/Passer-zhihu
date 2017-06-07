import time

Default_Headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36',
            'Host': 'www.zhihu.com',
            'authorization':'oauth c3cef7c66a1843f8b3a9e6a1e3160e20',
            'x-udid':'ADDCLchF5gqPTrrles-Rpkl2kO5Ec_2gXmc=',
            'Cookie':'d_c0="ADDCLchF5gqPTrrles-Rpkl2kO5Ec_2gXmc=|1480032023"; _zap=c3c080c8-e643-4adc-b1e3-aa1b4e57bfcd; _ga=GA1.2.849756013.1482491897; _xsrf=3761077c12b51b6e772218db942d2a49; q_c1=528deb3112164b36a9376d4cc7c376cb|1493683999000|1493683999000; aliyungf_tc=AQAAAGxKmhrQPwIAiGxZdab2xOQukhX+; acw_tc=AQAAABhhJSMhYQQAiGxZdaTOMCunmfas; capsion_ticket=451a25863bb54b95a05170699f7d9941'}

COOKIE = 'd_c0="ADDCLchF5gqPTrrles-Rpkl2kO5Ec_2gXmc=|1480032023"; _zap=c3c080c8-e643-4adc-b1e3-aa1b4e57bfcd; _ga=GA1.2.849756013.1482491897; _xsrf=3761077c12b51b6e772218db942d2a49; q_c1=528deb3112164b36a9376d4cc7c376cb|1493683999000|1493683999000; aliyungf_tc=AQAAAGxKmhrQPwIAiGxZdab2xOQukhX+; acw_tc=AQAAABhhJSMhYQQAiGxZdaTOMCunmfas; capsion_ticket=451a25863bb54b95a05170699f7d9941'
BASE_URL = 'https://www.zhihu.com'
ZHUANLAN_URL = 'https://zhuanlan.zhihu.com'

PHONE_LOGIN = BASE_URL + '/login/phone_num'
CAPTCHA_URL = BASE_URL+'/captcha.gif?r='+str(int(time.time())*1000)+'&type=login'

QUESTION_API = BASE_URL + '/api/v4/questions'
ANSWER_API = BASE_URL + '/api/v4/answers'

PERSOINFO_API = BASE_URL + '/people/'
MEMBER_API = BASE_URL + '/api/v4/members'

TOPIC_API = BASE_URL + '/topic/'
QUESTION_URL = BASE_URL + '/question/'

ZHUANLAN_ARTICLE = ZHUANLAN_URL + '/api/columns'
PROXIES = {'https':'1.1.1.1'}
ENG_FLAG = 'End'
HTML_TAG_REX = r'(<img.*?>)|(<a.*?</a>)|(<br>)|(</?blockquote>)|(</?noscript>)|(<p.*?</p>)|(<b.*?</b>)'