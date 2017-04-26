# encoding=utf8
import Util,urllib

class ThreadDeco(object):

	def __init__(self,func):
		self._func = func

	def __call__(self,*args):
		self._func(*args)
		while True:
			if not args[0].empty():
				page = args[0].get()
				if page == Util.ENG_FLAG:
					args[0].put(Util.ENG_FLAG)
					args[1].put(Util.ENG_FLAG)
					break

				res = args[2].get(page,headers=Util.Default_Headers)
				if res.status_code == 200:
					args[1].put(res)
					args[0].task_done()


def init_thread(url,pageCount,url_queue,s):
	ftype = url.split('/')[-1]
	offset,count_page = 1,0
	post_data = {'offset':offset,'limit':pageCount,'include':choose_include(ftype)}

	answer_data = urllib.parse.urlencode(post_data)
	r = s.get(url='{}?{}'.format(url,answer_data),headers=Util.Default_Headers)
	if r.status_code == 200:
		count_page = (int(r.json()['paging']['totals'])-1)//pageCount + 1
		
	for page in range(0,count_page):
		post_data['offset'] = page*pageCount + 1
		answer_data = urllib.parse.urlencode(post_data)
		url_queue.put('{}?{}'.format(url,answer_data))

def choose_include(ftype):
	if ftype == 'voters':
		return 'data[*].answer_count,articles_count,follower_count,gender,is_followed,is_following,badge[?(type=best_answerer)].topics'
	elif ftype == 'folowees' or ftype == 'followers':
		return 'data[*].answer_count,articles_count,gender,follower_count,is_followed,is_following,badge[?(type=best_answerer)].topics'
	elif ftype == 'favlists':
		return 'data[*].updated_time,answer_count,follower_count,creator,is_following'
	elif ftype == 'answers':
		return 'data[*].is_normal,is_sticky,collapsed_by,suggest_edit,comment_count,can_comment,content,editable_content,voteup_count,reshipment_settings,comment_permission,mark_infos,created_time,updated_time,relationship.is_authorized,is_author,voting,is_thanked,is_nothelp,upvoted_followees;data[*].author.badge[?(type=best_answerer)].topics'
	elif ftype == 'following-columns':
		return 'data[*].intro,followers,articles_count,image_url,image_width,image_height,is_following,last_article.created'
	elif ftype == 'following-questions' or ftype == 'questions':
		return 'data[*].created,answer_count,follower_count,author'
	else:
		return ''

@ThreadDeco
def thread_queue(urlqueue,htmlqueue,session):
	pass