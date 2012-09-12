#! /usr/bin/env python
# -*- coding: utf-8 -*-
from db_conf import *

class user_model(base_model):
    def _check_user_exist_by_name(self,username):
        return self.redis_client.exists(':'.join([self.USERNAME, username, self.UID]))

    def _get_user_id(self, username):
        return self.redis_client.get(':'.join([self.USERNAME, username,  self.UID]))

    def _get_user_name(self, uid):
        return self.redis_client.hget(':'.join([self.UID, uid, self.HASH]), self.USERNAME)

    def _get_user_headimage(self, uid):
        return self.redis_client.hget(':'.join([self.UID, uid, self.HASH]), self.HEADIMAGE)

    def _get_user_base_info(self, uid):
        return self.redis_client.hgetall(':'.join([self.UID, uid, self.HASH]))

    def _get_user_follower_list(self, uid):
        return self.redis_client.smembers(':'.join([self.UID, uid, self.FOLLOWER_LIST]))

    def _get_user_following_list(self, uid):
        return self.redis_client.smembers(':'.join([self.UID, uid, self.FOLLOWING_LIST]))

    def _add_follower(self, selfid, followerid):
        self.redis_client.sadd(':'.join([self.UID, selfid, self.FOLLOWER_LIST]), followerid)
    
    def _add_following(self, selfid, followingid):
        self.redis_client.sadd(':'.join([self.UID, selfid, self.FOLLOWING_LIST]), followingid)
    
    def _get_user_likes(self, uid):
        #TODO:
        pass

    def _add_like_video(self, uid, vid):
        self.redis_client.sadd(':'.join([self.UID, uid, self.LIKE_VIDEO_LIST]), vid)
    
    def _get_like_video_list(self, uid):
        return self.redis_client.smembers(':'.join([self.UID, uid, self.LIKE_VIDEO_LIST]))
    
if __name__ == '__main__':
    tmp = user_model()
    print tmp.UID
