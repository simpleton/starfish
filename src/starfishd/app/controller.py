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
