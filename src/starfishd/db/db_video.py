#! /usr/bin/env python
# -*- coding: utf-8 -*-
from db_conf import *

def _init_empty_video_info(vid):
    item = {SPOT:'null', POPULAR:'0', TITLE:'null', PUBLIC:'1', URL:'null', VIDEO_SHA1:'null', OWNER:'null', VID:'null'}
    redis_client.hmset(':'.join([VID, vid, HASH]), item)
    
    
def _set_video_title(vid, title):
    if (redis_client.exists(':'.join([VID, vid , HASH]))):
        redis_client.hset(':'.join([VID, vid, HASH]), TITLE, title)

def _set_video_spot(vid, vspot):
    if (redis_client.exists(':'.join([VID, vid, HASH]))):
        redis_client.hset(':'.join([VID, vid, HASH]), SPOT, vspot)

def _set_video_popular(vid , popular):
    if (redis_client.exists(':'.join([VID, vid , HASH]))):
        redis_client.hset(':'.join([VID, vid, HASH]), POPULAR, popular)

def _set_video_public(vid , authority):
    if (redis_client.exists(':'.join([VID, vid , HASH]))):
        #TODO: user check
        redis_client.hset(':'.join([VID, vid, HASH]), PUBLIC, authority)

def _get_video_title(vid):
    return redis_client.hget(':'.join([VID, vid, HASH]), TITLE)
    
def _get_video_spot(vid):
    return redis_client.hget(':'.join([VID, vid, HASH]), SPOT)

def _get_video_POPULAR(vid):
    return redis_client.hget(':'.join([VID, vid, HASH]), POPULAR)

def _get_video_public(vid):
    return redis_client.hget(':'.join([VID, vid, HASH]), PUBLIC)

def _get_video_url(vid):
    #TODO: implement me
    return 'www.soso.com'

def _get_video_owner(vid):
    return redis_client.hget(':'.join([VID, vid, HASH]), OWNER)

def _get_video_id(sha1):
    return redis_client.get(':'.join([VIDEO_SHA1, sha1, VID]))

def _get_video_sha1(vid):
    return redis_client.hget(':'.join([VID, vid, HASH]), VIDEO_SHA1)

def _del_video(vid):
    sha1 = _get_video_sha1(vid)
    redis_client.delete(':'.join([VID, vid, HASH]))
    redis_client.delete(':'.join([VIDEO_SHA1, sha1, VID]))

def _add_liked_user(vid, uid):
    redis_client.sadd(':'.join([VID, vid, LIKED_USER_LIST]), vid)
    
def _get_liked_user_list(vid):
    return redis_client.smembers(':'.join([VID, vid, LIKED_USER_LIST]))
