#! /usr/bin/env python
# -*- coding: utf-8 -*-
from db_conf import *
import gettime
from db_user import user_model as user

class video_model(base_model):
    def __init__(self):
        self.user_model = user()
        
    def _init_empty_video_info(self, vid):
        item = {self.SPOT:'null', self.POPULAR:'0', self.TITLE:'null', \
                self.PUBLIC:'1', self.URL:'null', self.VIDEO_SHA1:'null', \
                self.OWNER:'null', self.VID:'null'}
        self.redis_client.hmset(':'.join([self.VID, vid, self.HASH]), item)
        
    def _key_vid(self, vid):
        return ':'.join([self.VID, vid, self.HASH])
        
    def _check_video_existed(self, vid):
        if self.redis_client.exists(self._key_vid(vid)):
            return True    
        else:
            return False

    def _set_video_title(self, vid, title):
        if (self._check_video_existed(vid)):
            self.redis_client.hset(self._key_vid(vid), self.TITLE, title)

    def _set_video_spot(self, vid, vspot):
        if (self._check_video_existed(vid)):
            self.redis_client.hset(self._key_vid(vid), self.SPOT, vspot)

    def _set_video_popular(self, vid , popular):
        if (self._check_video_existed(vid)):
            self.redis_client.hset(self._key_vid(vid), self.POPULAR, popular)

    def _set_video_public(self, vid , authority):
        if (self._check_video_existed(vid)):
            #TODO: user check
            self.redis_client.hset(self._key_vid(vid), self.PUBLIC, authority)

    def _set_video_url(self, vid, url):
        if (self._check_video_existed(vid)):
            self.redis_client.hset(self._key_vid(vid), self.URL, url)

    def _set_video_thumb(self, vid, thumb_nail_url):
        if (self._check_video_existed(vid)):
            self.redis_client.hset(self._key_vid(vid), self.THUMB_NAIL, thumb_nail_url)

    def _get_video_title(self, vid):
        return self.redis_client.hget(self._key_vid(vid), self.TITLE)

    def _get_video_spot(self, vid):
        return self.redis_client.hget(self._key_vid(vid), self.SPOT)

    def _get_video_POPULAR(self, vid):
        return self.redis_client.hget(self._key_vid(vid), self.POPULAR)

    def _get_video_public(self, vid):
        return self.redis_client.hget(self._key_vid(vid), self.PUBLIC)

    def _get_video_url(self, vid):
        return self.redis_client.hget(self._key_vid(vid), self.URL)

    def _get_video_owner(self, vid):
        return self.redis_client.hget(self._key_vid(vid), self.OWNER)

    def _get_video_id(self, sha1):
        return self.redis_client.get(':'.join([self.VIDEO_SHA1, sha1, self.VID]))
    
    def _get_video_sha1(self, vid):
        return self.redis_client.hget(self._key_vid(vid), self.VIDEO_SHA1)

    def _del_video(self, vid):
        sha1 = _get_video_sha1(vid)
        self.redis_client.delete(self._key_vid(vid))
        self.redis_client.delete(':'.join([self.VIDEO_SHA1, sha1, self.VID]))

    def _add_liked_user(self, vid, uid):
        self.redis_client.sadd(':'.join([self.VID, vid, self.LIKED_VIDEO_USER_LIST]), uid)

    def _remove_liked_user(self, vid, uid):
        self.redis_client.srem(':'.join([self.VID, vid, self.LIKED_VIDEO_USER_LIST]), uid)

    def is_liked_user(self, vid, uid):
        return self.redis_client.sismember(':'.join([self.VID, vid, self.LIKED_VIDEO_USER_LIST]), uid)
    
    def _get_liked_user_list(self, vid):
        return self.redis_client.smembers(':'.join([self.VID, vid, self.LIKED_VIDEO_USER_LIST]))
    
    def _add_comment(self, username, vid, comment):
        now = gettime.gettime()
        mcomment = {'reviewer':username, 'content':comment, 'posttime':now.get()}
        self.redis_client.lpush(':'.join([self.VID, vid, self.COMMENT]), mcomment)
    
    def _get_comment(self, vid):
        comment_list = []
        comment_list = self.redis_client.lrange(':'.join([self.VID, vid, self.COMMENT]), 0, -1)
        for i, elem in zip(xrange(len(comment_list)), comment_list):
            elem = eval(elem)
            username = elem['reviewer']
            elem['reviewer'] = self.user_model._get_user_base_info(self.user_model._get_user_id(username))
            comment_list[i] = elem
        return comment_list

if __name__ == '__main__':
    tmp = video_model()
    tmp._get_comment('1')
    print tmp.UID
