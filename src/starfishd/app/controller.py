#! /usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = 'simsun'

import sys
sys.path.append('..')
from errorcode_builder import server_error as errorno
import os
import web
import json
import traceback
import hashlib
from decorator import *
from db.db import mmodel


class echo_test:
    """ only for  test"""
    def POST(self):
        d = web.input()
        return " %s " % json.dumps(d)
    
    def GET(self):
        d = web.input()
        return " %s " % (json.dumps(d))
        
    
class user_add:
    """add new user"""
    def POST(self):
        model = mmodel()
        try:
            data = json.loads(web.data())
            if (not model.check_user_exist_by_name(data['username'])):
                model.new_user(data['username'],data['head_image'])
            else:
                return "user already existed"
        except Exception as e:
            print traceback.print_exc()
            return e
        return " user_add %s " % db.db.get_user_base_info(data['username'])

class user:
    """query user dat
    """
    def GET(self, UID):
        tmp = db.db.get_user_base_info(UID)
        return tmp

class video:
    """query video info"""
    def GET(self, VID):
        model = mmodel()
        return model.get_video_base_info(VID)

class file_upload:
    def GET(self):
        return 'file_upload'
    def POST(self):
        try:
            model = mmodel()
            sha1 = hashlib.sha1()
            upfile    = web.input(uploaded_file={}, thumb_nail={})
            owner     = upfile.get('video_owner')
            place     = upfile.get('video_place')
            title     = upfile.get('video_title')
            authority = upfile.get('video_is_public')

            print owner,place,title,authority 
            urldir = '/video/'
            filedir = '/var/www' + urldir
#            print owner, sha1.hexdigest(), authority, title
            if not os.path.exists(filedir):
                os.mkdir(filedir)

            sha1.update(upfile.uploaded_file.value)      
            
            filepath = ''.join([filedir, sha1.hexdigest(), '.mp4'])
            with open(filepath, 'wb') as saved:
                saved.write(upfile.uploaded_file.file.read())

            filepath_thumb = ''.join([filedir, sha1.hexdigest(), '.png'])
            with open(filepath_thumb, 'wb') as thumb_file:
                thumb_file.write(upfile.thumb_nail.file.read())
                
            video_url = ''.join([urldir, sha1.hexdigest(), '.mp4'])
            thumb_url = ''.join([urldir, sha1.hexdigest(), '.png'])
            
            ret = model.new_video(owner, filepath, sha1.hexdigest(), title, place,url=video_url, thumb_url=thumb_url)
            if (ret == -1):
                return errorno.server_error(errorno.VIDEO_ALREADY_EXISTED[0], errorno.VIDEO_ALREADY_EXISTED[1])
            elif (ret == -2):
                return 'user not existed'

        except Exception as e:
            print traceback.print_exc()
            
            
        
class friend_add:
    def POST(self):
        try:
            model = mmodel()
            data = json.loads(web.data())
            if (model.check_user_exist_by_name(data['friend_name'])):
                #TODO:
                model.add_friend(data['username'],data['friend_name'])
            else:
                return errorno.server_error(errorno.VIDEO_NOT_EXISTED[0], errorno.VIDEO_NOT_EXISTED[1]).dumps()
        except Exception as e:
            print traceback.print_exc()
            return e
        return " user_add %s " % model.get_user_base_info(data['username'])
        
class video_list:
    @check_user_existed_byname
    def GET(self, username):
        model = mmodel()
        return model.get_video_list_byusername(username)
    
    def POST(self, username):
        model = mmodel()
        return model.get_video_list_byusername(username)

class user_following:
    @check_user_existed_byname
    def GET(self, username):
        model = mmodel()
        return model.get_user_following_list(username)

class user_follower:
    @check_user_existed_byname
    def GET(self, username):
        model = mmodel()
        return model.get_user_follower_list(username)

class user_likevideos:
    @check_user_existed_byname
    def GET(self, username):
        model = mmodel()
        return model.get_user_like_video_list(username)
      
class video_likeby_users:
    @check_video_exist_byid
    def GET(self, vid):
        model = mmodel()
        return model.get_videoliked_user_list(vid)
      
class video_comment:
    @check_video_exist_byid
    def GET(self, vid):
        model = mmodel()
        return model.get_comment(vid)

class all_video:
    @check_user_existed_byname
    def GET(self, username):
        model = mmodel()
        return model.get_all_video(username)


class upload_headimage:
    def POST(self):
        input_data = web.input(head_image={})
        model = mmodel()
        username = input_data.get('username')
        if (username != None) and (model.check_user_exist_by_name(username)):
            urldir = '/video/headimage/'
            filedir = '/var/www' + urldir
#            print owner, sha1.hexdigest(), authority, title
            if not os.path.exists(filedir):
                os.mkdir(filedir)

            filepath = "%s%s.png" % (filedir, username) 
            with open(filepath, 'wb') as image_file:
                image_file.write(input_data.head_image.file.read())
            
            headimage_url = "%s%s.png" % (urldir, username)
            return model.set_user_headimage(username, headimage_url)
        else :
            return 'no such user'
    
class like_video:
    def POST(self):
        input_data = web.input()
        username   = input_data.get('username')
        vid        = input_data.get('video_id')
        like       = input_data.get('like')
        model      = mmodel()
        
        if (like == '0'):
            model.like_video(username, vid)
        else:
            model.dislike_video(username, vid)
        

# class dislike_video:
#     @check_video_exist_byid
#     def POST(self, vid):
#         #TODO:
#         return 'NOT IMPLEMENT'

class comment:
    @check_video_exist_byid
    def POST(self, vid):
        #TODO:
        return 'NOT IMPLEMENT'
