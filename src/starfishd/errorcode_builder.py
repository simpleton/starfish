#! /usr/bin/env python
import json
__author__ = 'simsun'

import web



USER_NOT_EXISTED = 101, 'user not existed'

VIDEO_NOT_EXISTED = 201, 'video not existed'


class server_error:
    def __init__(self, *str):
        def init1(self,errorno):
            self.errorno = errorno
            self.desc = 'error'
            
        def init2(self, errorno, description):
            self.errorno = errorno
            self.desc = description
            
        if len(str)==2:
            init2(self, *str)
        else:
            init1(self, *str)
            
#    def __init__(self, errorno, error_description='error'):
#        self.errorno = errorno
#        self.desc = error_description
        
    def dumps(self):
        dict = {}
        dict['error_code'] = self.errorno
        dict['description'] = self.desc
        return json.dumps(dict)

if __name__ == "__main__":
    error = server_error(12, "test")
    print error.dumps()
   
