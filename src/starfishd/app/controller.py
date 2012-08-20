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
        param = web.input()
        try:
            db.db.new_user(param['id'],param['nick'],param['head_image'])
        except:
            #TODO:
            pass
        
        return " GUID = %s " % (json.dumps(param))

class user:
    """query user data"""
    def GET(self, UID):
        tmp = db.db.get_user_base_info(UID)
        print tmp
        return tmp


    
