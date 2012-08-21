#! /usr/bin/env python

__author__ = 'simsun'

import web
import json
import db.db
import traceback

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
        tmp = db.db.get_video_base_info(VID)
        print tmp
        return tmp

class video_add:
    """add new video"""
    def POST(self):
        try:
            video = web.input(myvideo={})
            data = json.loads(web.data())
            filedir = '/tmp/'
            filename = data['VIDEO_SHA1']
            with open(filedir.join(filename), 'wb') as saved:
                saved.write(video.myvideo.file.read())
        except Exception as e:
            print traceback.print_exc()
            return e

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
        
