#! /usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = 'xbfool'

import web
import json
from url_builder import url_builder
from db.db import db

urls = (
    '/echo',    'echo',
    '/list',    'list'
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
            tmp = db()
            return tmp.select(url)
            
application = app.wsgifunc()
if __name__ == "__main__":
    app.run()
