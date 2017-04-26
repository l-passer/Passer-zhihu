from Question import *
from User import *
from Answer import *
from Topic import *

user = User()
u = user.login('','')

# 一个获取问题所有回答相关信息的例子
Question('19698905',u).archieve_answerlist()

# 一个获取回答基本信息的例子，
# 还可以获取所有收藏该回答的收藏夹以及所有点赞用户
ans = Answer('https://www.zhihu.com/question/54446315/answer/159712952',u)
ans.archieve_answer_list('voters')

# 一个获取用户基本信息的例子
user.archieve_userinfo('shotgun')

# 一个用来获取用户所有粉丝和关注列表的例子关注的专栏和所有的提问等信息
'''
	followers,followees,following-columns,following-questions,asks
'''
user.archieve_list('ying-shi-tong-xue','questions')

# 一个用来获取话题所有精华问题的例子
Topic('19577498',u).archieve_topanswers()