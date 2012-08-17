__author__ = 'xbfool'

import web
import redis
from hello import hello
urls = (
    '/hello', 'hello',
    '/user/add/info', 'user_add',
#    '/user/set/info', 'user_update',
#    '/user/info/meta', 'user_info_meta',
#    '/user/info/all', 'user_info_all',
#    '/user/info/relation', 'user_info_relation',
#    '/user/set/likevideos', 'user_set_like_videos'
    )
app = web.application(urls, globals())
db  = redis.Redis(host='127.0.0.1',port=6379,db=1)


class user_add:
    def POST(self):
        pass

class user_update:
    def POST(self):
        pass

class user_info_meta:
    def GET(self):
        pass

class user_info_all:
    def GET(self):
        pass

class user_info_relation:
    def GET(self):
        pass

class user_set_like_videos:
    def POST(self):
        pass

class get_hotest_list:
    def GET(self,start,end):
        pass

class get_user_list:
    def GET(self,UID,start,end):
        pass

class get_video_comments:
    def GET(self,start,end):
        pass

class query_videos:
    def GET(self, condition, start, end):
        pass


    
application = app.wsgifunc()
if __name__ == "__main__":
    app.run()
