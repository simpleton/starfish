#! /usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = 'xbfool'

import web
import redis
import json
import app.controller

urls = (
    '/echo',                      'app.controller.echo_test',
    '/user/(\d+)',                'app.controller.user',
    '/user/add',                  'app.controller.user_add',
    '/user/friends/add',          'app.controller.friend_add',    
    '/video/(\d+)',               'app.controller.video',
    '/video/add',                 'app.controller.video_add',
    '/fileupload',                'app.controller.file_upload',
    '/video/list/username/(.*)',  'app.controller.video_list',
    '/user/following/(.*)',       'app.controller.user_following',
    '/user/follower/(.*)',        'app.controller.user_follower',
    '/user/video/like/(.*)',      'app.controller.user_likevideos',
    '/video/user/like/(.*)',      'app.controller.video_likeby_users',
    '/video/comment/(.*)',        'app.controller.video_comment',
    '/allvideo/(.*)',             'app.controller.all_video',
    '/user/headimage/(.*)',       'app.controller.upload_headimage',
    '/video/like/(\d+)',          'app.controller.like_video',
    '/video/dislike/(\d+)',       'app.controller.dislike_video',
    '/video/comment/(\d+)',       'app.controller.comment'
        
    )
app = web.application(urls, globals())
    
application = app.wsgifunc()
if __name__ == "__main__":
    app.run()
