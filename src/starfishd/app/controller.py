#! /usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = 'simsun'

import web
import json
import db.db
import traceback
import hashlib

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
            print data
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
        print tmp
        return tmp

class video:
    """query video info"""
    def GET(self, VID):
        print 'video'
        tmp = db.db.get_video_base_info(VID)
        print tmp
        return tmp

class video_add:
    """add new video"""
    def POST(self):
        try:
            print 'add new video'
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
        print 'upload file'
        upfile = web.input(uploaded_file={})
        filepath = 'hello'
        with open(filepath, 'wb') as saved:
            saved.write(upfile.uploaded_file.file.read())
            
        
class friend_add:
    def POST(self):
        try:
            data = json.loads(web.data())
            print data
            if (db.db.check_user_exist_by_name(data['friend_name'])):
                print "add friend"
                #TODO:
                db.db.add_friend(data['username'],data['friend_name'])
            else:
                print "user not existed"
                return "user not existed"
        except Exception as e:
            print traceback.print_exc()
            return e
        return " user_add %s " % db.db.get_user_base_info(data['username'])
        
class video_list:
    def GET(self, username):
        print username
        return db.db.get_video_list_byusername(username)
    
    def POST(self, username):
        return db.db.get_video_list_byusername(username)

        
