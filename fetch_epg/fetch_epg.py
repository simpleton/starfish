#! /usr/bin/env python
# -*- coding: utf-8 -*-

from url_builder import url_builder
import urllib2
import re
from HTMLParser import HTMLParser

class MyParser(HTMLParser):
    def __init__(self):
        HTMLParser.__init__(self)
        self.video_list = []
        self.pattern = re.compile('(([1-9]{1})|([0-1][0-9])|([1-2][0-3])):([0-5][0-9])')
        self.list = []
    def handle_starttag(self, tag, attrs):
        pass
                
    def handle_data(self, data):
        data = data.strip()
        if not (data == ''):
            filter_data = self.check_item_format(data)
            if filter_data:
                self.video_list.append(filter_data)
        
    def print_video_list(self):
        for elem in self.video_list:
            print elem[0], unicode(elem[1], 'utf-8')

    def check_item_format(self, item):
        #start with time,such as 12:12
        print item
        epg_item = self.pattern.match(item)
        if epg_item == None:
            return False
        else:
            show_time = epg_item.group(0)
            ret = show_time, item.lstrip(show_time)
            if not (ret[1] == '-12:00' or ret[1] == '-24:00'):
                return ret
            else :
                return False
            
if __name__ == '__main__':
    full_url = url_builder('cctv1',day_delta=0).build()
    html_data = urllib2.urlopen(full_url).read()
    my = MyParser()
    my.feed(html_data)
    my.print_video_list()
    

