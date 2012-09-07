#! /usr/bin/env python
# -*- coding: utf-8 -*-
import urllib
from datetime import datetime

class url_builder:
    def __init__(self, channel, day_delta = 0):
        self.day_delta        = day_delta
        self.param            = {}
        self.domain           = 'http://tv.cntv.cn/index.php'
        self.param['action']  = 'epg-list'
        self.param['date']    = self._get_current_date()
        self.param['channel'] = channel
        
    def build(self):
        url_param = urllib.urlencode(self.param)
        full_url  = ''.join([self.domain, '?', url_param])
        return full_url

    def _get_current_date(self):
        now = datetime.now().timetuple()
        return '-'.join([str(now.tm_year), str(now.tm_mon), str(now.tm_mday + self.day_delta)])

if __name__ == '__main__':
    url = url_builder('cctv1').build()
    print url
