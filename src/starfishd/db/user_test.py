#! /usr/bin/env python
# -*- coding: utf-8 -*-
import unittest
#from db_video import video_model
import test
from db_user import user_model as user

class user_testcase(unittest.TestCase):
    def setUp(self):
        self.user_model = user()
        
    def test_user_model_string(self):
        tmp = self.user_model
        self.assertEqual(tmp.UID , 'uid')
        self.assertEqual(tmp.HASH, 'hash')
     
    def test_check_exist(self):
        name = 'thisnamecannotexists'  
        self.assertFalse(self.user_model._check_user_exist_by_name(name))
        

if __name__ == "__main__":
    suite1 = unittest.TestLoader().loadTestsFromTestCase( \
             user_testcase)
    suite2 = unittest.TestLoader().loadTestsFromTestCase( \
             test.video_singal_query_testcase)
    suite = unittest.TestSuite([suite1, suite2])
    unittest.TextTestRunner().run(suite)
