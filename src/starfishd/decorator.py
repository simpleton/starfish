#! /usr/bin/env python
# -*- coding: utf-8 -*-

import db.db
import errorcode_builder as errorno

def trace(f, *args, **kw):
    print 'call %s with args %s,%s' % (f.__name__, args, kw)
    return f(*args, **kw)

def check_user_existed_byname(func):
    def check(self, username, *args):
        if (db.db.check_user_exist_by_name(username)):
            return func(self, username, *args)
        else:
            return errorno.server_error(errorno.USER_NOT_EXISTED[0], errorno.USER_NOT_EXISTED[1]).dumps()
    return check

def check_video_exist_byid(func):
    def check(self, vid, *args):
        if (db.db.check_video_exist_by_id(vid)):
            return func(self, vid, *args)
        else:
            return errorno.server_error(errorno.VIDEO_NOT_EXISTED[0], errorno.VIDEO_NOT_EXISTED[1]).dumps()
    return check


def check_user_and_vid(func):
    def check(username, videoid, *args):
        if (not db.db.check_user_exist_by_name(username)):
            return errorno.server_error(errorno.USER_NOT_EXISTED[0], errorno.USER_NOT_EXISTED[1]).dumps()
        elif (not db.db.check_video_exist_by_id(videoid)):
            return errorno.server_error(errorno.VIDEO_NOT_EXISTED[0], errorno.VIDEO_NOT_EXISTED[1]).dumps()
        else:
            return func(username, vid, *args)
    return check
