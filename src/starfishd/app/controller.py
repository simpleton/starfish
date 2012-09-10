#! /usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = 'simsun'

import os
import web
import json
import db.db
import traceback
import hashlib
import errorcode_builder as errorno
from decorator import *


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
        try:
            data = json.loads(web.data())
            if (not db.db.check_user_exist_by_name(data['username'])):
                print "add user"
                db.db.new_user(data['username'],data['head_image'])
            else:
                print "user already existed"
                return "user already existed"
        except Exception as e:
            print traceback.print_exc()
            return e
        return " user_add %s " % db.db.get_user_base_info(data['username'])

class user:
    """query user data"""
    def GET(self, UID):
        tmp = db.db.get_user_base_info(UID)
        return tmp

class video:
    """query video info"""
    def GET(self, VID):
        tmp = db.db.get_video_base_info(VID)
        return tmp

class video_add:
    """add new video"""
    def POST(self):
        try:
            sha1 = hashlib.sha1()
            video = web.input(upfile={})
            data = web.data()
            filedir = '/tmp/'
            filepath = filedir.join(data['VIDEO_SHA1'])
            owner = data['owner']
            with open(filepath, 'wb') as saved:
                sha1.update(video.upfile.file.read())
                if (sha1.hexdigest() == data['VIDEO_SHA1']):
                    db.db.new_video(owner, filepath, data['VIDEO_SHA1'])
                    saved.write(video.upfile.file.read())
                else:
                    print "upload error"
                    return 'upload error'
        except Exception as e:
            print traceback.print_exc()
            return e

class file_upload:
    def GET(self):
        return 'file_upload'
    def POST(self):
        try:
            sha1 = hashlib.sha1()
            upfile    = web.input(uploaded_file={}, thumb_nail={})
            owner     = upfile.get('video_owner')
            place     = upfile.get('video_place')
            title     = upfile.get('video_title')
            authority = upfile.get('video_is_public')

            print owner,place,title,authority 
            filedir = '/var/www/video/'
#            print owner, sha1.hexdigest(), authority, title
            if not os.path.exists(filedir):
                os.mkdir(filedir)

            sha1.update(upfile.uploaded_file.file.read())      
            filepath = ''.join([filedir, sha1.hexdigest(), '.mp4'])
            with open(filepath, 'wb') as saved:
                print upfile.uploaded_file.file.read()
                saved.write(upfile.uploaded_file.file.read())
                ret = db.db.new_video(owner, filepath, sha1.hexdigest(), title, place)
                print 'add new video ', ret
                if (ret == -1):
                    return errorno.server_error(errorno.VIDEO_ALREADY_EXISTED[0], errorno.VIDEO_ALREADY_EXISTED[1])
                elif (ret == -2):
                    return 'user not existed'
            filepath_thumb = ''.join([filedir,'thumb',sha1.hexdigest(), '.png'])
            with open(filepath_thumb, 'wb') as thumb_file:
                thumb_file.write(upfile.thumb_nail.file.read())
        except Exception as e:
            print traceback.print_exc()
            
            
        
class friend_add:
    def POST(self):
        try:
            data = json.loads(web.data())
            if (db.db.check_user_exist_by_name(data['friend_name'])):
                #TODO:
                db.db.add_friend(data['username'],data['friend_name'])
            else:
                return errorno.server_error(errorno.VIDEO_NOT_EXISTED[0], errorno.VIDEO_NOT_EXISTED[1]).dumps()
        except Exception as e:
            print traceback.print_exc()
            return e
        return " user_add %s " % db.db.get_user_base_info(data['username'])
        
class video_list:
    @check_user_existed_byname
    def GET(self, username):
        return db.db.get_video_list_byusername(username)
    
    def POST(self, username):
        return db.db.get_video_list_byusername(username)

class user_following:
    @check_user_existed_byname
    def GET(self, username):
        return db.db.get_user_following_list(username)

class user_follower:
    @check_user_existed_byname
    def GET(self, username):
        return db.db.get_user_follower_list(username)

class user_likevideos:
    @check_user_existed_byname
    def GET(self, username):
        return db.db.get_user_like_video_list(username)
      
class video_likeby_users:
    @check_video_exist_byid
    def GET(self, vid):
        return db.db.get_videoliked_user_list(vid)
      
class video_comment:
    @check_video_exist_byid
    def GET(self, vid):
        return db.db.get_comment(vid)

class all_video:
    @check_user_existed_byname
    def GET(self, username):
        return db.db.get_all_video(username)
