#! /usr/bin/python
# -*- coding: utf-8 -*-
import json
import web
import redis
from db_user import user_model
from db_video import video_model
import gettime
from db_conf import *

#decorator
def check_user_and_vid(func):
    def check(self, username, videoid, *args):
        if (not self.check_user_exist_by_name(username)):
            return errorno.server_error(errorno.USER_NOT_EXISTED[0], \
                                        errorno.USER_NOT_EXISTED[1]).dumps()
        elif (not self.check_video_exist_by_id(videoid)):
            return errorno.server_error(errorno.VIDEO_NOT_EXISTED[0], \
                                        errorno.VIDEO_NOT_EXISTED[1]).dumps()
        else:
            func(self, username, videoid, *args)
    return check
    
class mmodel(base_model):
    def __init__(self):
        self.user  = user_model()
        self.video = video_model() 
            
    def check_user_exist_by_name(self, username):
        return self.user._check_user_exist_by_name(username)

    def check_video_exist_by_id(self, vid):
        return self.video._check_video_existed(vid)

    def new_user(self, username, head_image):
        if (self.redis_client.exists(':'.join([self.USERNAME,username,self.UID]))):
            #already in database
            return False
        else :
            userid = str(self.redis_client.incr(self.GLOBAL_USERID_FLAG))
            print ':'.join([self.USERNAME,username,self.UID])

            self.redis_client.set(':'.join([USERNAME, username,  self.UID]), userid)
            userinfo = {self.USERNAME  : username,
                        self.HEADIMAGE : head_image,
                        self.UID       :userid}
            self.redis_client.hmset(':'.join([self.UID, userid, self.HASH]), userinfo)
            return True

    def get_user_base_info(self, username):
        #self.redis_client.get(':'.join([self.USERNAME, username,  self.UID]))
        uid = self.user._get_user_id(username)
        return self.user._get_user_base_info(uid)

    def _print_all_user(self):
        print self.redis_client.keys()

    def _new_video(self, owner, filepath, sha1):
        if (not self.check_user_exist_by_name(owner)):
            return -2
        elif (not self.redis_client.exists(':'.join([self.VIDEO_SHA1, sha1, self.VID]))):
            vid = str(self.redis_client.incr(self.GLOBAL_VIDEOID_FLAG))
            self.video._init_empty_video_info(vid)
            self.redis_client.set(':'.join([self.VIDEO_SHA1, sha1, self.VID]), vid)

            now  = gettime.gettime()
            self.redis_client.set(':'.join([self.VID, vid, self.PUBLIC_TIME]), now.get())
            
            info = {self.VID        :vid, 
                    self.VIDEO_SHA1 :sha1, 
                    self.OWNER      :owner, 
                    self.PUBLIC_TIME:now.get()}
            self.redis_client.hmset(':'.join([self.VID, vid, self.HASH]), info)

            uid = self.user._get_user_id(owner)
            self.redis_client.lpush(':'.join([self.UID, uid, self.VIDEO_LIST]), vid)
            return vid
        else:
            #already in database
            return -1
    
    def new_video(self, owner, filepath, sha1, title, spot, is_hot='0', \
                  is_public='1',url='/video/1.mp4',thumb_url='/video/default.png'):
                  
        vid = self._new_video(owner, filepath, sha1)
        if (vid > 0):
            self.video._set_video_spot(vid, spot)
            self.video._set_video_title(vid, title)
            self.video._set_video_popular(vid, is_hot)
            self.video._set_video_public(vid, is_public)
            self.video._set_video_url(vid, url)
            self.video._set_video_thumb(vid, thumb_url)
            return vid
        else :
            return vid
    
    def add_follow(self, selfname, friendname):
        selfid   = self.user._get_user_id(selfname)
        friendid = self.user._get_user_id(friendname)
        self._add_follow(selfid, friendid)
    
    def _add_follow(self, selfid, friendid):
        self.user._add_following(selfid, friendid)
        self.user._add_follower(friendid, selfid)

    def like_video(self, username, videoid):
        uid = self.user._get_user_id(username)
        self.user._add_like_video(uid, videoid)
        self.video._add_liked_user(videoid, uid)

    def get_videoliked_user_list(self, vid):
        if (self.video._check_video_existed(vid)):
            userlist = self.video._get_liked_user_list(vid)
            return json.dumps(self._get_json_user_list(userlist))
        else:
            return server_error(1,"no such user").dumps()

    def get_user_like_video_list(self, username):
        uid     = self.user._get_user_id(username)
        vidlist = self.user._get_like_video_list(uid)
        return json.dumps(self._get_json_video_list(vidlist))

    @check_user_and_vid
    def add_comment(self, username, videoid, comment):
        return self.video._add_comment(username, videoid, comment)
    
    def get_comment(self, vid):
        commentlist = self.video._get_comment(vid)
        mdict = {}
        mdict['error_code'] =  '0'
        mdict['total_size'] = len(commentlist)
        mdict['comment'] = commentlist
        return json.dumps(mdict)
    
    def get_user_follower_list(self, username):
        uid = self.user._get_user_id(username)
        mlist = self.user._get_user_follower_list(uid)
        return json.dumps(self._get_json_user_list(mlist))

    def get_user_following_list(self, username):
        uid = self.user._get_user_id(username)
        mlist = self.user._get_user_following_list(uid)
        return json.dumps(self._get_json_user_list(mlist))
    
    def _get_json_user_list(self, uidlist):
        mdict = {}
        user_list = []
        for uid in uidlist:
            user_list.append(self.user._get_user_base_info(uid))
        mdict['error_code'] = '0'
        mdict['people'] = user_list
        mdict['total_size'] = len(uidlist)
        return mdict

    def get_video_base_info(self, vid):
        baseinfo          = self.redis_client.hgetall(':'.join([self.VID, vid, self.HASH]))
        baseinfo['owner'] = self.get_user_base_info(baseinfo['owner'])
        return baseinfo

    def get_video_list_byuserid(self, uid):
        video_list = self.redis_client.lrange(':'.join([self.UID, uid, self.VIDEO_LIST]),0 ,-1)
        return video_list

    def get_video_list_byusername(self, username):
        uid                 = self.user._get_user_id(username)
        vid_list            = self.get_video_list_byuserid(uid)
        return self._get_json_video_list(vid_list)

    def _get_json_video_list(self, vidlist):
        video_list = []
        for vid in vidlist:
            video_list.append(self.get_video_base_info(vid))
        mdict = {}
        mdict['error_code'] = '0'
        mdict['video_list'] = video_list
        mdict['total_size'] = len(vidlist)
        return mdict
    
    def _get_json_video_list_sortedbydate(self, vidlist,username):
        video_list = []
        for vid in vidlist:
            video_list.append(vid)
            self.redis_client.sadd(':'.join([self.USERNAME, username, self.SORTEDLIST]), vid)
            #    for elem in _get_json_video_list(video_list)['video_list']:
            #        print elem[PUBLIC_TIME]
            #    print self.redis_client.smembers(':'.join([self.USERNAME, username, SORTEDLIST]))
        sorted_list = self.redis_client.sort(':'.join([self.USERNAME,username, self.SORTEDLIST]) , \
                                        desc=True, \
                                        by=':'.join([':'.join([self.VID, '*', self.PUBLIC_TIME])]))

        for elem in self._get_json_video_list(sorted_list)['video_list']:
            print elem[self.PUBLIC_TIME]
        return self._get_json_video_list(sorted_list)
    
    def get_all_video(self, username):
        video_list = []
        uid = self.user._get_user_id(username)
        userlist = self.user._get_user_following_list(uid)    
        userlist.add(uid)
        vid_list = []
        for i in userlist:
            vid_list.extend(self.get_video_list_byuserid(i))
        return json.dumps(self._get_json_video_list_sortedbydate(vid_list, username))
    
    def _clear_all(self):
        for elem in self.redis_client.keys():
            self.redis_client.delete(elem)
    
if __name__ == '__main__':
    now = gettime.gettime()
    print now.get()
    tmp = model()
    tmp.new_user('simsun', "www.soso.com")

    tmp._clear_all()
    tmp._print_all_user()
