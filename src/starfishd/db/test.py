#! /usr/bin/env python
# -*- coding: utf-8 -*-
import unittest
from db_conf import *
import db
import db_video
import db_user

class video_singal_query_testcase(unittest.TestCase):
    def setUp(self):
        self.SHA1 = 'AABBCC2'
        db.new_user('simsun', "www.soso.com")
        db.new_user('tyler', 'www.tyler.com')
        db.new_user('juncheng', 'www.juncheng.com')
        db.new_video('simsun', 'test123', self.SHA1, 'title1', 'spot1')
        db.new_video('simsun', 'video1', self.SHA1+'A', 'title2', 'spot2')
        db.new_video('simsun', 'video2', self.SHA1+'B', 'title3', 'spot3')
        db.new_video('simsun', 'video3', self.SHA1+'C', 'title4', 'spot5')
        db.new_video('juncheng', 'video1', self.SHA1+'D', 'title5', 'spot6')
        db._new_video('juncheng', 'video_juncheng', self.SHA1+'E')
        db.add_follow('simsun', 'tyler')
        db.add_follow('simsun', 'juncheng')
        db.like_video('simsun', '1')
        db.like_video('simsun', '2')
        db.like_video('tyler', '1')
        db.like_video('juncheng', '1')


    def tearDown(self):
        vid = db_video._get_video_id(self.SHA1)
        #db_video._del_video(vid)
        
    def test_like_video_userlist(self):
        userlist = db.get_videoliked_user_list('2')
        print 'test_like_video', userlist
        userlist = db.get_videoliked_user_list('1')
        print userlist
        
    def test_user_liked_videolist(self):
        videolist = db.get_user_like_video_list('simsun')
        print videolist
        videolist = db.get_user_like_video_list('tyler')
        print videolist
        
    def test_new_video(self):
        SHA1   = self.SHA1
        vid    = db_video._get_video_id(SHA1)
        title  = 'test_title'
        spot   = 'spot'
        public = 'public'
        self.assertEqual(db_video._get_video_id(SHA1), vid)
        db_video._set_video_title(vid, title)
        db_video._set_video_spot(vid, spot)
        db_video._set_video_public(vid, '0')
        self.assertEqual(db_video._get_video_spot(vid), spot)
        self.assertEqual(db_video._get_video_title(vid), title)
        
    def test_modify_property(self):
        SHA1   = self.SHA1
        title  = 'test_title1'
        spot   = 'spot1'
        public = 'public1'
        vid    = db_video._get_video_id(SHA1)
        self.assertEqual(db_video._get_video_id(SHA1), vid)
        db_video._set_video_title(vid, title)
        db_video._set_video_spot(vid, spot)
        db_video._set_video_public(vid, '0')
        self.assertEqual(db_video._get_video_spot(vid), spot)
        self.assertEqual(db_video._get_video_title(vid), title)
#        print db.get_video_base_info(vid)
        
    def test_get_base_info(self):
        SHA1 = self.SHA1
        vid  = db_video._get_video_id(SHA1)
        print db.get_video_base_info(vid)

    def test_get_videolist(self):
        SHA1 = self.SHA1
        print db.get_video_list_byusername('simsun')

    def test_follow_list(self):
        print 'follower list:', db.get_user_follower_list('simsun')
        print 'following list:', db.get_user_following_list('simsun')

    def test_add_comment(self):
        print db.add_comment('simsun', '1', 'great video')
        print db.add_comment('tyler', '1', 'great!!') 
        print db.add_comment('tyler', '1', 'great!!') 
        print db.add_comment('tyler', '1', 'great!!') 
        print db.get_comment('1')
        
if __name__ == '__main__':
    unittest.main()
