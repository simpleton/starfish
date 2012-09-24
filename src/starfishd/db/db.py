#! /usr/bin/python
# -*- coding: utf-8 -*-
import sys
sys.path.append('..')
from errorcode_builder import server_error as errorno
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
            return errorno(errorno.USER_NOT_EXISTED[0], \
                                        errorno.USER_NOT_EXISTED[1]).dumps()
        elif (not self.check_video_exist_by_id(videoid)):
            return errorno(errorno.VIDEO_NOT_EXISTED[0], \
                                        errorno.VIDEO_NOT_EXISTED[1]).dumps()
        else:
            return func(self, username, videoid, *args)
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
        return self.user.new_user(username, head_image)
        
    def del_user(self, username):
        uid = self.user._get_user_id(username)
        return self.user.remove_user(uid)
        
    def get_user_base_info(self, username):
        #self.redis_client.get(':'.join([self.USERNAME, username,  self.UID]))
        uid = self.user._get_user_id(username)
        return self.user._get_user_base_info(uid)

    def _print_all_user(self):
        print self.redis_client.keys()

    def set_user_headimage(self, username, image_url):
        uid = self.user._get_user_id(username)
        return self.user.set_headimage(uid, image_url)
        
    def get_user_headimage(self, username):
        uid = self.user._get_user_id(username)
        return self.user.get_headimage(uid)
    
    def _new_video(self, owner, filepath, sha1):
        return self.video._new_video(owner, filepath, sha1)
    
    def new_video(self, owner, filepath, sha1, title, spot, is_hot='0', \
                  is_public='1',url='/video/1.mp4',thumb_url='/video/default.png'):
        return self.video.new_video(owner, filepath, sha1, title, spot ,is_hot, is_public, url, thumb_url)
    
    def del_video(self, vid):
        self.video._del_video(vid)
    
    def add_follow(self, selfname, friendname):
         if (not self.check_user_exist_by_name(selfname))  \
             or (not self.check_user_exist_by_name(friendname)):
             return errorno(errorno.USER_NOT_EXISTED[0], \
                            errorno.USER_NOT_EXISTED[1]).dumps()

         selfid   = self.user._get_user_id(selfname)
         friendid = self.user._get_user_id(friendname)
         self._add_follow(selfid, friendid)

    def del_follow(self, selfname, friendname):
         if (not self.check_user_exist_by_name(selfname))  \
             or (not self.check_user_exist_by_name(friendname)):
             return errorno.server_error(errorno.USER_NOT_EXISTED[0], \
                                         errorno.USER_NOT_EXISTED[1]).dumps()

         selfid   = self.user._get_user_id(selfname)
         friendid = self.user._get_user_id(friendname)
         self._del_follow(selfid, friendid)

    def _add_follow(self, selfid, friendid):
        self.user._add_following(selfid, friendid)
        self.user._add_follower(friendid, selfid)
    
    def _del_follow(self, selfid, friendid):
        self.user.del_following(selfid, friendid)
        self.user.del_follower(friendid, selfid)
    
    @check_user_and_vid
    def like_video(self, username, videoid):
        uid = self.user._get_user_id(username)
        self.user._add_like_video(uid, videoid)
        self.video._add_liked_user(videoid, uid)
        
    @check_user_and_vid
    def dislike_video(self, username, videoid):
        uid = self.user._get_user_id(username)
        self.user._remove_like_video(uid, videoid)
        self.video._remove_liked_user(videoid, uid)
        
    @check_user_and_vid
    def is_user_like_video(self, username, videoid):
        uid = self.user._get_user_id(username)
        if (self.user.is_like_video(uid ,videoid)   \
            and self.video.is_liked_user(videoid, uid)):
            print 'user_like_video'
            return True
        elif (not self.user.is_like_video(uid, videoid))  \
             and (not self.video.is_liked_user(videoid, uid)):
            print 'user_dislike_video'
            return False
        else:
            print "like status exist inconsistent!!!"
            return False
    
    
    def get_videoliked_user_list(self, vid):
        if (self.video._check_video_existed(vid)):
            userlist = self.video._get_liked_user_list(vid)
            return json.dumps(self._get_json_user_list(userlist))
        else:
            return errorno(1,"no such user").dumps()

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
        #baseinfo only save the username , that isn't enough
        baseinfo['owner'] = self.get_user_base_info(baseinfo['owner'])
        baseinfo['liked_num'] = self.video.get_liked_user_number(vid)
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
    tmp = mmodel()
    #tmp._clear_all()
    tmp._print_all_user()
