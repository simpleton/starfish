#! /usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = 'simsun'

import web
import json
from url_builder import url_builder
from db.db import db

urls = (
    '/echo',    'echo',
    '/list',    'list',
    '/showing', 'showing_list'
    )
app = web.application(urls, globals())

class echo:
    def GET(self):
        input_data = web.input()
        return input_data.get('an')
        
class list:
    def GET(self):
        input_data = web.input()
        channel    = input_data.get('channel')
        date       = input_data.get('date')
        
        if (not channel) or (not date):
            return 'error'
        else:
            url = url_builder(channel).set_data_by_str(date).build()
            model               = db()
            mdict               = {}
            mdict['date']       = date
            mdict['channel']    = channel
            mdict['list']       = []
            plist               = model.select(url)
            mdict['total_size'] = len(plist)
            for prog in plist:
                tmp = {}
                prog = eval(prog)
                tmp['time'] = prog[0]
                tmp['name'] = prog[1]
                mdict['list'].append(tmp)
                
            return json.dumps(mdict)

class showing_list:
    def GET(self):
        mdict                 = {}
        program_list,now      = db().get_showing_list()
        mdict['total_size']   = len(program_list)
        mdict['list']         = program_list
        mdict['current_time'] = now
        return json.dumps(mdict)
    
application = app.wsgifunc()
if __name__ == "__main__":
    app.run()
