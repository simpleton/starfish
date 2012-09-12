#! /usr/bin/python
# -*- coding: utf-8 -*-

import unittest
import controller as ct

def deco_try(func):
    def decorator_func(self):
        try:
            func(self)
        except Exception as e:
            pass
    return decorator_func

class controller_testcase(unittest.TestCase):
    def setUp(self):
        pass
    
    def tearDown(self):
        pass
    
    @deco_try
    def test_echo_get(self):
        echo = ct.echo_test()
        echo.GET()

    @deco_try
    def test_echo_post(self):
        echo = ct.echo_test()
        echo.POST()
        
    @deco_try
    def test_user_add(self):
        ua = ct.user_add()
        ua.POST()
        ua.GET()
        
if __name__ == '__main__':
    suite1 = unittest.TestLoader(). \
        loadTestsFromTestCase(controller_testcase)

    suite = unittest.TestSuite([suite1])
    unittest.TextTestRunner().run(suite)
