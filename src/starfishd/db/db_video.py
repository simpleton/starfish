#! /usr/bin/env python
# -*- coding: utf-8 -*-
from db_conf import *
import gettime
import db_user

class video_model(base_model):
    def _init_empty_video_info(vid):
        item = {self.SPOT:'null', self.POPULAR:'0', self.TITLE:'null', \
                self.PUBLIC:'1', self.URL:'null', self.VIDEO_SHA1:'null', \
                self.OWNER:'null', self.VID:'null'}
        self.redis_client.hmset(':'.join([self.VID, vid, self.HASH]), item)

    def _check_video_existed(vid):
        if (self.redis_client.exists(':'.join([self.VID, vid, self.HASH]))):
            return True    
        else:
            return False

    def _set_video_title(vid, title):
        if (_check_video_existed(vid)):
            self.redis_client.hset(':'.join([self.VID, vid, self.HASH]), self.TITLE, title)

    def _set_video_spot(vid, vspot):
        if (_check_video_existed(vid)):
            self.redis_client.hset(':'.join([self.VID, vid, self.self.HASH]), self.SPOT, vspot)

    def _set_video_popular(vid , popular):
        if (_check_video_existed(vid)):
            self.redis_client.hset(':'.join([self.VID, vid, self.HASH]), self.POPULAR, popular)

    def _set_video_public(vid , authority):
        if (_check_video_existed(vid)):
            #TODO: user check
            self.redis_client.hset(':'.join([self.VID, vid, self.HASH]), self.PUBLIC, authority)

    def _set_video_url(vid, url):
        if (_check_video_existed(vid)):
            self.redis_client.hset(':'.join([self.VID, vid, self.HASH]), self.URL, url)

    def _set_video_thumb(vid, thumb_nail_url):
        if (_check_video_existed(vid)):
            self.redis_client.hset(':'.join([self.VID, vid, self.HASH]), self.THUMB_NAIL, thumb_nail_url)

    def _get_video_title(vid):
        return self.redis_client.hget(':'.join([self.VID, vid, self.HASH]), self.TITLE)

    def _get_video_spot(vid):
        return self.redis_client.hget(':'.join([self.VID, vid, self.HASH]), self.SPOT)

    def _get_video_POPULAR(vid):
        return self.redis_client.hget(':'.join([self.VID, vid, self.HASH]), self.POPULAR)

    def _get_video_public(vid):
        return self.redis_client.hget(':'.join([self.VID, vid, self.HASH]), self.PUBLIC)

    def _get_video_url(vid):
        return self.redis_client.hget(':'.join([self.VID, vid, self.HASH]), self.URL)

    def _get_video_owner(vid):
        return self.redis_client.hget(':'.join([self.VID, vid, self.HASH]), self.OWNER)

    def _get_video_id(sha1):
        return self.redis_client.get(':'.join([self.VIDEO_SHA1, sha1, self.VID]))
    
    def _get_video_sha1(vid):
        return self.redis_client.hget(':'.join([self.VID, vid, self.HASH]), self.VIDEO_SHA1)

    def _del_video(vid):
        sha1 = _get_video_sha1(vid)
        self.redis_client.delete(':'.join([self.VID, vid, self.HASH]))
        self.redis_client.delete(':'.join([self.VIDEO_SHA1, sha1, self.VID]))

    def _add_liked_user(vid, uid):
        self.redis_client.sadd(':'.join([self.VID, vid, LIKED_VIDEO_USER_LIST]), uid)

    def _get_liked_user_list(vid):
        return self.redis_client.smembers(':'.join([self.VID, vid, LIKED_VIDEO_USER_LIST]))
    
    def _add_comment(username, vid, comment):
        now = gettime.gettime()
        mcomment = {'reviewer':username, 'content':comment, 'posttime':now.get()}
        self.redis_client.lpush(':'.join([self.VID, vid, COMMENT]), mcomment)
    
    def _get_comment(vid):
        comment_list = []
        comment_list = self.redis_client.lrange(':'.join([self.VID, vid, COMMENT]), 0, -1)
        for i, elem in zip(xrange(len(comment_list)), comment_list):
            elem = eval(elem)
            username = elem['reviewer']
            elem['reviewer'] = db_user._get_user_base_info(db_user._get_user_id(username))
            comment_list[i] = elem
        return comment_list

