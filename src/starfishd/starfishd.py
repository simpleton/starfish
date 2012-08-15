__author__ = 'xbfool'

import web

urls = (
    '/', 'hello',
#    '/user/add/info', 'user_add',
#    '/user/set/info', 'user_update',
#    '/user/info/meta', 'user_info_meta',
#    '/user/info/all', 'user_info_all',
#    '/user/info/relation', 'user_info_relation',
#    '/user/set/likevideos', 'user_set_like_videos'
    )
app = web.application(urls, globals())

class hello:
    def GET(self):

        return 'Hello !'

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

application = app.wsgifunc()
if __name__ == "__main__":
    app.run()
