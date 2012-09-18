#! /usr/bin/env python
# -*- coding: utf-8 -*-
import unittest
from db import mmodel
from user_test import *
from db_video import video_model
from db_user import user_model
import time

class video_singal_query_testcase(unittest.TestCase):
    def setUp(self):
        self.SHA1 = 'AABBCC2'
        self.db = mmodel() 
        self.video = video_model()
        self.user = user_model()
        print type(self.db)
        self.db.new_user('simsun', "www.soso.com")
        self.db.new_user('tyler', 'www.tyler.com')
        self.db.new_user('juncheng', 'www.juncheng.com')
        self.db.new_user('test1', 'www.test1.com')
        self.db.new_user('test2', 'www.test2.com')
        self.db.new_user('test3', 'www.test3.com')
        self.db.new_user('test4', 'www.test4.com')
        self.db.new_user('test5', 'www.test5.com')
        self.db.new_user('test6', 'www.test6.com')
        self.db.new_user('test7', 'www.test7.com')
        self.db.new_user('test8', 'www.test8.com')
        self.db.new_user('test9', 'www.test9.com')
        
        self.db.new_video('simsun', 'test123', self.SHA1, 'title1', 'spot1', url='/video/1.mp4')
        self.db.new_video('simsun', 'video1', self.SHA1+'A', 'title2', 'spot2', url='/video/2.mp4')
        self.db.new_video('simsun', 'video2', self.SHA1+'B', 'title3', 'spot3', url='/video/3.mp4')
        self.db.new_video('simsun', 'video3', self.SHA1+'C', 'title4', 'spot5', url='/video/4.mp4')
        self.db.new_video('juncheng', 'video1', self.SHA1+'D', 'title5', 'spot6', url='/video/5.mp4')
        self.db._new_video('juncheng', 'video_juncheng', self.SHA1+'E')
        self.db.new_video('tyler', 'video', self.SHA1+'EF', 'title', 'spot1', url='/video/6.mp4')
        self.db.new_video('tyler', 'video', self.SHA1+'F', 'title', 'spot2', url='/video/7.mp4')
        self.db.new_video('tyler', 'video', self.SHA1+'Z', 'title', 'spot3',url='/video/1.mp4')
        self.db.add_follow('simsun', 'tyler')
        self.db.add_follow('simsun', 'juncheng')
        self.db.add_follow('simsun', 'test1')
        self.db.add_follow('simsun', 'test2')
        self.db.add_follow('simsun', 'test3')
        self.db.add_follow('simsun', 'test4')
        self.db.add_follow('simsun', 'test5')
        self.db.add_follow('simsun', 'test6')
        self.db.add_follow('simsun', 'test7')
        self.db.add_follow('simsun', 'test8')
        self.db.add_follow('simsun', 'test9')
        self.db.del_follow('simsun', 'tyler')
        self.db.add_follow('test1', 'simsun')
        self.db.add_follow('test2', 'simsun')
        self.db.add_follow('test3', 'simsun')
        self.db.add_follow('test4', 'simsun')
        self.db.add_follow('test5', 'simsun')
        self.db.add_follow('test6', 'simsun')
        self.db.add_follow('test7', 'simsun')
        self.db.add_follow('test8', 'simsun')
        self.db.add_follow('test9', 'simsun')
        self.db.like_video('simsun', '1')
        self.db.like_video('simsun', '2')
        self.db.like_video('tyler', '1')
        self.db.like_video('juncheng', '1')
        


    def tearDown(self):
        vid = self.video._get_video_id(self.SHA1)
        #self.db_video._del_video(vid)
        
    def test_like_video_userlist(self):
        userlist = self.db.get_videoliked_user_list('2')
        print 'test_like_video', userlist
        userlist = self.db.get_videoliked_user_list('1')
        print userlist
        
    def test_user_liked_videolist(self):
        videolist = self.db.get_user_like_video_list('simsun')
        print videolist
        videolist = self.db.get_user_like_video_list('tyler')
        print videolist
        
    def test_new_video(self):
        SHA1   = self.SHA1
        vid    = self.video._get_video_id(SHA1)
        title  = 'test_title'
        spot   = 'spot'
        public = 'public'
        self.assertEqual(self.video._get_video_id(SHA1), vid)
        self.video._set_video_title(vid, title)
        self.video._set_video_spot(vid, spot)
        self.video._set_video_public(vid, '0')
        self.assertEqual(self.video._get_video_spot(vid), spot)
        self.assertEqual(self.video._get_video_title(vid), title)
        
    def test_modify_property(self):
        SHA1   = self.SHA1
        title  = 'test_title1'
        spot   = 'spot1'
        public = 'public1'
        vid    = self.video._get_video_id(SHA1)
        self.assertEqual(self.video._get_video_id(SHA1), vid)
        self.video._set_video_title(vid, title)
        self.video._set_video_spot(vid, spot)
        self.video._set_video_public(vid, '0')
        self.assertEqual(self.video._get_video_spot(vid), spot)
        self.assertEqual(self.video._get_video_title(vid), title)
#        print db.get_video_base_info(vid)
        
    def test_get_base_info(self):
        SHA1 = self.SHA1
        vid  = self.video._get_video_id(SHA1)
        print self.db.get_video_base_info(vid)

    def test_get_videolist(self):
        SHA1 = self.SHA1
        print self.db.get_video_list_byusername('simsun')

    def test_follow_list(self):
        print 'follower list:', self.db.get_user_follower_list('simsun')
        print 'following list:', self.db.get_user_following_list('simsun')

    def test_add_comment(self):
        print self.db.add_comment('simsun', '1', 'great video')
        print self.db.add_comment('tyler', '1', 'great!!') 
        print self.db.add_comment('tyler', '1', 'great!!') 
        print self.db.add_comment('tyler', '1', 'great!!') 
        print self.db.get_comment('1')

    def test_like_video(self):
        self.db.like_video('simsun','1')
    
    def test_dislike_video(self):
        self.db.dislike_video('simsun', '1')
        
    def test_is_user_like_video(self):
        self.db.like_video('simsun', '1')
        self.assertTrue(self.db.is_user_like_video('simsun', '1'))
        
        self.db.dislike_video('simsun', '1')
        self.assertFalse(self.db.is_user_like_video('simsun', '1'))
        
    def test_modify_head_image(self):
        testurl = '/video/test.png'
        self.db.set_user_headimage('simsun', testurl)
        self.assertEqual(testurl, self.db.get_user_headimage('simsun'))
    
if __name__ == "__main__":
    suite1 = unittest.TestLoader().loadTestsFromTestCase( \
             user_testcase)
    suite2 = unittest.TestLoader().loadTestsFromTestCase( \
             video_singal_query_testcase)
    suite = unittest.TestSuite([suite1, suite2])
    unittest.TextTestRunner().run(suite)

