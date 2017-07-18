# vim: set et ts=4 sw=4
# coding: utf8
# !/usr/bin/python
import os
import sys
import json
import unittest
import sys
sys.path.append('../')
from jsonparser import decoder
# from jsonparser import JSONEncoder

JSONDecoder = decoder.JSONDecoder

class DecoderTest(unittest.TestCase):

    def test_empty_string(self):
        test_str = ''
        parser = JSONDecoder()
        with self.assertRaises(ValueError):
            parser.decode(test_str)

    def test_empty_obj(self):
        test_str = '{}'
        parser = JSONDecoder()
        self.assertDictEqual(json.loads(test_str), parser.decode(test_str))

    def test_simple_obj(self):
        test_str = '{"abc" : "cba"}' # {u'abc' : u'cba'}
        parser = JSONDecoder()
        self.assertDictEqual(json.loads(test_str), parser.decode(test_str))

    def test_constant(self):
        test_str = '{"abc" : {"cde" : {"null": null, "true": true, "false": false  }}}'
        parser = JSONDecoder()
        self.assertDictEqual(json.loads(test_str), parser.decode(test_str))

    def test_obj_list(self):
        test_str = '{"abc" : {"cde" : [1,2,3,4]}}'
        parser = JSONDecoder()
        self.assertDictEqual(json.loads(test_str), parser.decode(test_str))

if __name__ == '__main__':
    unittest.main()
