#! /usr/bin/env python
# -*- coding: utf-8 -*-
from db_conf import *

class user_model(base_model):
    def new_user(self, username, head_image):
        if (self.redis_client.exists(':'.join([self.USERNAME,username,self.UID]))):
            print 'already in database'
            return False
        else :
            userid = str(self.redis_client.incr(self.GLOBAL_USERID_FLAG))
            self.redis_client.set(':'.join([self.USERNAME, username,  self.UID]), userid)
            userinfo = {self.USERNAME  : username,
                        self.HEADIMAGE : head_image,
                        self.UID       :userid}
            self.redis_client.hmset(':'.join([self.UID, userid, self.HASH]), userinfo)
            return True
        
    def remove_user(self, uid):
        username = self._get_user_name(uid)
        self.redis_client.delete(':'.join([self.UID, uid, self.HASH]))
        self.redis_client.delete(':'.join([self.USERNAME, username, self.UID]))
        self.redis_client.delete(':'.join([self.UID, uid, self.VIDEO_LIST]))
    
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
    
    def del_follower(self, selfid, followerid):
        self.redis_client.srem(':'.join([self.UID, selfid, self.FOLLOWER_LIST]), followerid)
    
    def _add_following(self, selfid, followingid):
        self.redis_client.sadd(':'.join([self.UID, selfid, self.FOLLOWING_LIST]), followingid)
    
    def del_following(self, selfid, followingid):
        self.redis_client.srem(':'.join([self.UID, selfid, self.FOLLOWING_LIST]), followingid)
    
    def _get_user_likes(self, uid):
        #TODO:
        pass

    def _add_like_video(self, uid, vid):
        self.redis_client.sadd(':'.join([self.UID, uid, self.LIKE_VIDEO_LIST]), vid)
        
    def _remove_like_video(self, uid, vid):
        self.redis_client.srem(':'.join([self.UID, uid, self.LIKE_VIDEO_LIST]), vid)    
        
    def is_like_video(self, uid ,vid):
        return self.redis_client.sismember(':'.join([self.UID, uid, self.LIKE_VIDEO_LIST]), vid)
        
    def _get_like_video_list(self, uid):
        return self.redis_client.smembers(':'.join([self.UID, uid, self.LIKE_VIDEO_LIST]))
    
    def set_headimage(self, uid, image_url):
        return self.redis_client.hset(':'.join([self.UID, uid, self.HASH]), self.HEADIMAGE, image_url)
    
    def get_headimage(self, uid):
        return self.redis_client.hget(':'.join([self.UID, uid, self.HASH]), self.HEADIMAGE)
    
if __name__ == '__main__':
    tmp = user_model()
    print tmp.UID
