#! /usr/bin/python
# -*- coding: utf-8 -*-
import json
import web
import redis
import db_video
import db_user
from db_conf import *
from datetime import datetime

def new_user(username, head_image):
    if (redis_client.exists(':'.join([USERNAME,username,UID]))):
        #already in database
        return False
    else :
        userid = str(redis_client.incr(GLOBAL_USERID_FLAG))
        print ':'.join([USERNAME,username,UID])
    
        redis_client.set(':'.join([USERNAME, username,  UID]), userid)
        userinfo = {USERNAME:username, HEADIMAGE:head_image, UID:userid}
        redis_client.hmset(':'.join([UID, userid, HASH]), userinfo)
        return True

def get_user_base_info(username):
    #redis_client.get(':'.join([USERNAME, username,  UID]))
    uid = db_user._get_user_id(username)
    return db_user._get_user_base_info(uid)

def check_user_exist_by_name(username):
    return redis_client.exists(':'.join([USERNAME,  username, UID]))

def _print_all_user():
    print redis_client.keys()

def _new_video(owner, filepath, sha1):
    if (not redis_client.exists(':'.join([VIDEO_SHA1, sha1, VID]))):
        vid = str(redis_client.incr(GLOBAL_VIDEOID_FLAG))
        db_video._init_empty_video_info(vid)
        redis_client.set(':'.join([VIDEO_SHA1, sha1, VID]), vid)

        now  = datetime.now()
        info = {VID:vid, VIDEO_SHA1:sha1, OWNER:owner, PUBLIC_TIME:now}
        redis_client.hmset(':'.join([VID, vid, HASH]), info)

        uid = db_user._get_user_id(owner)
        redis_client.lpush(':'.join([UID, uid, VIDEO_LIST]), vid)
        return vid
    else:
        #already in database
        return -1
    
def new_video(owner, filepath, sha1, title, spot, is_hot='0', is_public='1'):
    vid = _new_video(owner, filepath, sha1)
    if (vid > 0):
        db_video._set_video_spot(vid, spot)
        db_video._set_video_title(vid, title)
        db_video._set_video_popular(vid, is_hot)
        db_video._set_video_public(vid, is_public)
        return vid
    else :
        return -1    
    
def add_follow(selfname, friendname):
    selfid   = db_user._get_user_id(selfname)
    friendid = db_user._get_user_id(friendname)
    _add_follow(selfid, friendid)
    
def _add_follow(selfid, friendid):
    db_user._add_following(selfid, friendid)
    db_user._add_follower(friendid, selfid)

def like_video(username, videoid):
    uid = db_user._get_user_id(username)
    db_user._add_like_video(uid, videoid)
    db_video._add_liked_user(videoid, uid)

def get_like_video_list(username):
    uid = db_user._get_user_id(username)
    return db_user._get_like_video_list(uid)

def get_liked_user_list(vid):
    return db_video._get_liked_user_list(vid)
    
def add_comment(username, videoid, comment):
    pass

def get_user_follower_list(username):
    uid = db_user._get_user_id(username)
    return db_user._get_user_follower_list(uid)

def get_user_following_list(username):
    uid = db_user._get_user_id(username)
    return db_user._get_user_following_list(uid)
    
def get_video_base_info(vid):
    baseinfo          = redis_client.hgetall(':'.join([VID, vid, HASH]))
    baseinfo['owner'] = get_user_base_info(baseinfo['owner'])
    return baseinfo

def get_video_list_byuserid(uid):
    video_list = redis_client.lrange(':'.join([UID, uid, VIDEO_LIST]),0 ,-1)
    return video_list

def get_video_list_byusername(username):
    uid                 = db_user._get_user_id(username)
    vid_list            = get_video_list_byuserid(uid)
    video_list          = []
    for i in vid_list:
        video_list.append(get_video_base_info(i))
    mdict               = {}
    mdict['error_code'] = '0'
    mdict['video_list'] = video_list
    mdict['total_size'] = len(vid_list)
    return json.dumps(mdict)
    
def _clear_all():
    for elem in redis_client.keys():
        redis_client.delete(elem)
    
if __name__ == '__main__':
    _clear_all()
    _print_all_user()
