#! /usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = 'simsun'

import web
import json
from url_builder import url_builder
from db.db import db
from fetch_epg import EPG
urls = (
    '/echo',    'echo',
    '/list',    'channel_list',
    '/showing', 'showing_list',
    '/show',    'certaintime_list'
    )
app = web.application(urls, globals())
epg = EPG()

class echo:
    def GET(self):
        input_data = web.input()
        return input_data.get('an')
        
class channel_list:
    def GET(self):
        input_data = web.input()
        channel    = input_data.get('channel')
        date       = input_data.get('date')
        model      = db()
        
        if (not channel) or (not date):
            return 'error'
        else:
            url = url_builder(channel).set_data_by_str(date).build()
            
            if (not model.select(url)):
                epg.get(date)
                
            plist = model.select(url)
            if (plist):
                mdict               = {}
                mdict['date']       = date
                mdict['channel']    = channel
                mdict['list']       = []
                mdict['total_size'] = len(plist)
                for prog in plist:
                    tmp              = {}
                    prog             = eval(prog)
                    tmp['time']      = prog[0]
                    tmp['name']      = prog[1]
                    tmp['cover_url'] = "www.qq.com"
                    mdict['list'].append(tmp)
                return json.dumps(mdict)
            else:
                return 'no keys' 
        
    
                

class showing_list:
    def GET(self):
        mdict                 = {}
        program_list,now      = db().get_showing_list()
        for elem in program_list:
            elem['cover_url'] = "www.qq.com"
        mdict['total_size']   = len(program_list)
        mdict['list']         = program_list
        mdict['current_time'] = now
        return json.dumps(mdict)
    
class certaintime_list:
    def GET(self):
        mdict      = {}
        input_data = web.input()
        day_time   = input_data.get('daytime')
        clock_time = input_data.get('clocktime')
        
        program_list,query_time = db().get_certaintime_list(clock_time, day_time)
        
        for elem in program_list:
            elem['cover_url'] = "www.qq.com"
        mdict['total_size']   = len(program_list)
        mdict['list']         = program_list
        mdict['query_time'] = query_time
        return json.dumps(mdict)
        
application = app.wsgifunc()
if __name__ == "__main__":
    app.run()
