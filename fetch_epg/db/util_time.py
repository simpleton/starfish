#! /usr/bin/env python
# -*- coding: utf-8 -*-

from datetime import datetime
from urlparse import urlparse, parse_qs

class mytime:
    def __init__(self):
        pass
    
    def str2num(self, time):
        """the format is (xx:xx)"""
        hour,min = time.split(':')
        return int(hour)*60 + int(min)

    def get_time(self, list, pos):
        """get the time of the pos th element in list with minutes. the list`s format must be [('xx:xx','content'),......]"""
        return self.str2num(eval(list[pos])[0])
    
    def get_now_in_day(self):
        """return year-month-day"""
        now = datetime.now().timetuple()
        now_str = '-'.join([ str(now.tm_year), str(now.tm_mon), str(now.tm_mday)])
        return now_str

    def get_now_in_minute(self):
        """return hour:minute"""
        now = datetime.now().timetuple()
        now_hour_min = ':'.join([str(now.tm_hour), str(now.tm_min)])
        return now_hour_min
        

    def get_date_from_url(self, url):
        """get the date parameter in url"""
        return self.get_param_from_url(url,'date')
    
    def get_param_from_url(self, url, param_name):
        url_param = parse_qs(urlparse(url).query)
        return url_param.get('date')[0]
         
if __name__ == '__main__':
    mytime = mytime()
    print mytime.get_date_from_url('http://localhost/epg/list?date=2012-9-11&channel=cctv1')
