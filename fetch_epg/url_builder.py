#! /usr/bin/env python
# -*- coding: utf-8 -*-
import urllib
from datetime import datetime,timedelta

class url_builder:
    def __init__(self, channel, day_delta = 0):
        self.day_delta        = day_delta
        self.param            = {}
        self.domain           = 'http://tv.cntv.cn/index.php'
        self.param['action']  = 'epg-list'
        self.param['date']    = self._get_current_date()
        self.param['channel'] = channel
        
    def set_data(self, year , month, day):
        self.param['date'] = '-'.join(str(year), str(month), str(day))
        return self
    
    def set_data_by_str(self, date_str):
        """the format of date_str should be yyyy-mm-dd"""
        self.param['date'] = date_str
        return self
    
    def build(self):
        url_param = urllib.urlencode(self.param)
        full_url  = ''.join([self.domain, '?', url_param])
        return full_url

    def _get_current_date(self):
        #now = datetime.now().timetuple()
        now = datetime.now()
        delta = timedelta(days=self.day_delta)
        future = (now + delta).timetuple()
        return '-'.join([str(future.tm_year), str(future.tm_mon), str(future.tm_mday)])

if __name__ == '__main__':
    url = url_builder('cctv1').build()
    print url
