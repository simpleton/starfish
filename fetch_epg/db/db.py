#! /usr/bin/env python
# -*- coding: utf-8 -*-
import sys
sys.path.append('..')
import redis
from url_builder import url_builder

class db:
    def __init__(self):
        self.client = redis.Redis(host='127.0.0.1', port=6379, db=2)

    def insert(self, url, program):
        for elem in program:
            self.client.rpush(url, elem)

    def select(self, url):
        return self.client.lrange(url, 0, -1)

    def _dump_all_keys(self):
        for i in  self.client.keys():
            print i
            for j in self.select(i):
                j = eval(j)
                print j[0], unicode(j[1], 'utf-8')
                
    def _clear_all(self):
        for i in self.client.keys():
            self.client.delete(i)
            
if __name__ == '__main__':
    tmp = db()
    tmp._dump_all_keys()
#    tmp._clear_all()
#    url = url_builder('cctv2').build()
#    print tmp.select(url)
