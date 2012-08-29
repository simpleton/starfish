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
    follower_list = redis_client.hget(':'.join([UID, uid, HASH]), FOLLOWER_LIST)
    return redis_client.smembers(follower_list)

def _get_user_following_list(uid):
    following_list = redis_client.hget(':'.join([UID, uid, HASH]), FOLLOWING_LIST)
    return redis_client.smembers(following_list)

def _add_follower(selfid, followerid):
    list_follower = redis_client.hget(':'.join([UID, selfid, HASH]), FOLLOWER_LIST )
    redis_client.sadd(list_follower, followerid)
    
def _add_following(selfid, followingid):
    list_following = redis_client.hget(':'.join([UID, selfid, HASH]), FOLLOWING_LIST)
    redis_client.sadd(list_following, followingid)
    
def _get_user_likes(uid):
    #TODO:
    pass
