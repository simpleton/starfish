#! /usr/bin/env python
# -*- coding: utf-8 -*-
from db_conf import *

def _get_user_id(username):
    return redis_client.get(':'.join([USERNAME, username,  UID]))

def _get_user_name(uid):
    return redis_client.hget(':'.join([UID, uid, HASH]), USERNAME)

def _get_user_headimage(uid):
    return redis_client.hget(':'.join([UID, uid, HASH]), HEADIMAGE)

def _get_user_base_info(uid):
    return redis_client.hgetall(':'.join([UID, uid, HASH]))

def _get_user_follower_list(uid):
    return redis_client.smembers(':'.join([UID, uid, FOLLOWER_LIST]))

def _get_user_following_list(uid):
    return redis_client.smembers(':'.join([UID, uid, FOLLOWING_LIST]))

def _add_follower(selfid, followerid):
    redis_client.sadd(':'.join([UID, selfid, FOLLOWER_LIST]), followerid)
    
def _add_following(selfid, followingid):
    redis_client.sadd(':'.join([UID, selfid, FOLLOWING_LIST]), followingid)
    
def _get_user_likes(uid):
    #TODO:
    pass

def _add_like_video(uid, vid):
    redis_client.sadd(':'.join([UID, uid, LIKE_VIDEO_LIST]), vid)
    
def _get_like_video_list(uid):
    return redis_client.smembers(':'.join([UID, uid, LIKE_VIDEO_LIST]))
    
