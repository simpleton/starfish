#! /usr/bin/env python
# -*- coding: utf-8 -*-

from db.db import mmodel


if __name__ == "__main__":
    namelist = ['simsun', 'tyler', 'juncheng', 'haoxu', 'xbfu', 'peter',  \
                'jamie', 'somebody', 'helloworld', 'smith', 'this_is_longest_name_all_over_the_world']
    model = mmodel()
    for user in namelist:
        model.new_user(user, 'www.baidu.com')
    for user in namelist:
        for otheruser in namelist:
            if user != otheruser:
                model.add_follow(user,otheruser)

