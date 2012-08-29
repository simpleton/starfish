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
        db.new_video('simsun', 'test123', self.SHA1)
        db.new_video('simsun', 'video1', self.SHA1+'A')
        db.new_video('simsun', 'video2', self.SHA1+'B')
        db.new_video('simsun', 'video3', self.SHA1+'C')
        db.new_video('juncheng', 'video1', self.SHA1+'D')
        db.new_video('juncheng', 'video_juncheng', self.SHA1+'E')
        db.add_follow('simsun', 'tyler')
        db.add_follow('simsun', 'juncheng')

    def tearDown(self):
        vid = db_video._get_video_id(self.SHA1)
        #db_video._del_video(vid)
        
    def test_new_video(self):
        SHA1   = self.SHA1
        vid    = db_video._get_video_id(SHA1)
        title  = 'test_title'
        spot   = 'spot'
        public = 'public'
        self.assertEqual(db_video._get_video_id(SHA1), vid)
        db_video._set_video_title(vid, title)
        db_video._set_video_spot(vid, spot)
        db_video._set_video_public(vid, spot)
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
        db_video._set_video_public(vid, spot)
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
        
            
if __name__ == '__main__':
    unittest.main()
