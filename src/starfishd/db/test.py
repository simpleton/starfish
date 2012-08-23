import unittest
from db_conf import *
import db
import db_video
class video_singal_query_testcase(unittest.TestCase):
    def setUp(self):
        self.SHA1 = 'AABBCC'
        db.new_video('simsun', 'test123', self.SHA1)

    def tearDown(self):
        vid = db_video._get_video_id(self.SHA1)
        db_video._del_video(vid)
        
    def test_new_video(self):
        SHA1 = self.SHA1
        vid = db_video._get_video_id(SHA1)
        print vid
        title = 'test_title'
        spot = 'spot'
        public = 'public'
        self.assertEqual(db_video._get_video_id(SHA1), vid)
        db_video._set_video_title(vid, title)
        db_video._set_video_spot(vid, spot)
        db_video._set_video_public(vid, spot)
        self.assertEqual(db_video._get_video_spot(vid), spot)
        self.assertEqual(db_video._get_video_title(vid), title)
        
    def test_modify_property(self):
        SHA1 = self.SHA1
        title = 'test_title1'
        spot = 'spot1'
        public = 'public1'
        vid = db_video._get_video_id(SHA1)
        self.assertEqual(db_video._get_video_id(SHA1), vid)
        db_video._set_video_title(vid, title)
        db_video._set_video_spot(vid, spot)
        db_video._set_video_public(vid, spot)
        self.assertEqual(db_video._get_video_spot(vid), spot)
        self.assertEqual(db_video._get_video_title(vid), title)
        print db.get_video_base_info(vid)
        
    def test_get_base_info(self):
        SHA1 = self.SHA1
        vid = db_video._get_video_id(SHA1)
        print db.get_video_base_info(vid)

if __name__ == '__main__':
    unittest.main()
