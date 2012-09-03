#! /usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = 'xbfool'

import web
import redis
import json
import app.controller

urls = (
    '/echo',        'app.controller.echo_test',
    '/user/(\d+)',  'app.controller.user',
    '/user/add',    'app.controller.user_add',
    '/user/friends/add', 'app.controller.friend_add',    
    '/video/(\d+)', 'app.controller.video',
    '/video/add',   'app.controller.video_add',
    '/fileupload',  'app.controller.file_upload',
    '/video/list/username/(.*)', 'app.controller.video_list',
    '/user/following/(.*)', 'app.controller.user_following',
    '/user/follower/(.*)', 'app.controller.user_follower',
    '/user/video/like/(.*)', 'app.controller.user_likevideos',
    '/video/user/like/(.*)', 'app.controller.video_likeby_users',
    '/video/comment/(.*)', 'app.controller.video_comment'
#    '/user/add/info', 'user_add',
#    '/user/set/info', 'user_update',
#    '/user/info/meta', 'user_info_meta',
#    '/user/info/all', 'user_info_all',
#    '/user/info/relation', 'user_info_relation',
#    '/user/set/likevideos', 'user_set_like_videos'
    )
app = web.application(urls, globals())


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
