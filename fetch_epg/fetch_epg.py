#! /usr/bin/env python
# -*- coding: utf-8 -*-

from url_builder import url_builder
import urllib2
import re
from conf import channel
from HTMLParser import HTMLParser
from db.db import db

class MyParser(HTMLParser):
    def __init__(self):
        HTMLParser.__init__(self)
        self.video_list = []
        self.pattern = re.compile('(([1-9]{1})|([0-1][0-9])|([1-2][0-3])):([0-5][0-9])')
        
    def _clean_(self):
        self.video_list = []
        
    def handle_starttag(self, tag, attrs):
        pass
                
    def handle_data(self, data):
        data = data.strip()
        if not (data == ''):
            filter_data = self.check_item_format(data)
            if filter_data:
                self.video_list.append(filter_data)
        
    def _print_video_list(self):
        for elem in self.video_list:
            print elem[0], unicode(elem[1], 'utf-8')
            
    def get_video_list(self):
        return self.video_list
        
    def check_item_format(self, item):
        #start with time,such as 12:12
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
            
class EPG:
    def __init__(self):
        self.channel = channel()
        self.model        = db()
        self.epg_parser   = MyParser()

    def get(self, date):
        """the format of date is yyyy-mm-dd"""
        for i in channel:
            full_url = url_builder(i).set_data_by_str(date).build()
            html_data = urllib2.urlopen(full_url).read()
            self.epg_parser._clean_()
            self.epg_parser.feed(html_data)
            self.model.insert(full_url, self.epg_parser.get_video_list())
    
    def get_today(self):
        """the format of date is yyyy-mm-dd"""
        for i in self.channel:
            full_url = url_builder(i).build()
            html_data = urllib2.urlopen(full_url).read()
            self.epg_parser._clean_()
            self.epg_parser.feed(html_data)
            self.model.insert(full_url, self.epg_parser.get_video_list())

if __name__ == '__main__':
    EPG().get_today()
    
#     channel = channel()
#     epg_db = db()
#     epg_parser = MyParser()
#     for i in channel:
#         full_url = url_builder(i, day_delta=0).build()
#         html_data = urllib2.urlopen(full_url).read()
#         epg_parser._clean_()
#         epg_parser.feed(html_data)
#         epg_db.insert(full_url, epg_parser.get_video_list())
# #        epg_parser.print_video_list()

 
   
