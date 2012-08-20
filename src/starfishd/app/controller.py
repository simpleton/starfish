#! /usr/bin/env python

__author__ = 'simsun'

import web
import json
import db.db

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
        data = json.loads(web.data())
        if (not db.db.check_user_exist(data['id'])):
            try:
                db.db.new_user(data['id'],data['nick'],data['head_image'])
            except:
                return "paramter Error"
        else:
            return "user already existed"
        return " user_add %s " % db.db.get_user_base_info(data['id'])

class user:
    """query user data"""
    def GET(self, UID):
        tmp = db.db.get_user_base_info(UID)
        print tmp
        return tmp


    
