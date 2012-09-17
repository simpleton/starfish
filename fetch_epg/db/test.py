#! /usr/bin/env python
# -*- coding: utf-8 -*-
import unittest
import db
class epg_db_testcase(unittest.TestCase):
    def setUp(self):
        self.model = db.db()
    
    def tearDown(self):
        pass
    
    def test_fetch_9_18(self):
        print self.model.get_certaintime_list('00:00', '2012-9-18')
        
if __name__ == '__main__':
    suite1 = unittest.TestLoader().loadTestsFromTestCase( \
             epg_db_testcase)
    suite = unittest.TestSuite([suite1])
    unittest.TextTestRunner().run(suite)
 

