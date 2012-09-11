#! /usr/bin/env python
# -*- coding: utf-8 -*-
import sys
sys.path.append('..')
import redis
import traceback
import json
from util_time import mytime
from url_builder import url_builder

class db:
    def __init__(self):
        self.client = redis.Redis(host='127.0.0.1', port=6379, db=2)
        self.mytime = mytime()


    def insert(self, url, program):
        if (not self.client.exists(url)):
            for elem in program:     
                self.client.rpush(url, elem)
                try:
                    insert_date = self.mytime.get_date_from_url(url)
                    self.client.sadd(':'.join(['DATA', insert_date, 'SET']), url)
                except Exception as e:
                    print traceback.print_exc()
                
    
    def select(self, key):
        if (self.client.exists(key)):
            return self.client.lrange(key, 0, -1)
        else:
#            """we should query fetch"""
#            date_days = self.mytime.get_date_from_url(key)
#            self.epg.get(date_days)
#            if (self.client.exists(key)):
#                return self.client.lrange(key, 0, -1)
#            else:
#                return 'can not load'
            return False

    def _dump_all_keys(self):
        for i in  self.client.keys():
            print i
            #for j in self.select(i):
            #    j = eval(j)
            #    print j[0], unicode(j[1], 'utf-8')
                
    def _dump_someday_keys(self, date):
        return self.client.smembers(':'.join(['DATA', date, 'SET']))
        
    def _clear_all(self):
        for i in self.client.keys():
            self.client.delete(i)

    def get_showing_list(self):
        now_day = self.mytime.get_now_in_day()
        now_hour_min = self.mytime.get_now_in_minute()
        mlist = []
        for url in self._dump_someday_keys(now_day):
            mdict = {}
            item = self._find_showing(self.select(url) ,now_hour_min)
            mdict['channel'] = self.mytime.get_param_from_url(url,'channel')
            
            if item:
                item = eval(item)
                mdict['time'] = item[0]
                mdict['program'] = item[1]
                #print item[0], unicode(item[1], 'utf-8')
            else:
                mdict['time'] = '24:00'
                mdict['program'] = 'no program'
            mlist.append(mdict)
        return (mlist, now_hour_min)
    
    def _find_showing(self, list, time):
        """the format of the element of list is (time, program_name)"""
        end   = len(list)
        start = 0
        pos   = (start+end)/2
        time = self.mytime.str2num(time)
        #binary search
        while start <= end and end > 0:
            #print time
            #print start , pos ,end
            if (self.mytime.get_time(list, pos) <= time) and  \
               (self.mytime.get_time(list, pos+1) > time):
                 break
            else:
                if self.mytime.get_time(list, pos+1) < time:
                    start = pos + 1
                else:
                    end = pos
                pos = (start+end)/2
                
        if (self.mytime.get_time(list, pos) <= time):
            return list[pos]
        else:
            return False
        
        
if __name__ == '__main__':
    tmp = db()
    tmp._dump_all_keys()
    #tmp._clear_all()
    tmp.get_showing_list()
#    url = url_builder('cctv2').build()
#    print tmp.select(url)
