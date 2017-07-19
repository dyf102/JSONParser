# vim: set et ts=4 sw=4
# coding: utf8
# !/usr/bin/python
import sys
import json
import unittest
import os
sys.path.append('../')
from jsonparser import decoder
from jsonparser import encoder
from jsonparser import jsonparser
JSONDecoder = decoder.JSONDecoder
JSONEncoder = encoder.JSONEncoder
JSONParser = jsonparser.JSONParser


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
        test_str = '{"abc" : "cba"}'  # {u'abc' : u'cba'}
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


class EncoderTest(unittest.TestCase):

    def test_null(self):
        test_obj = None
        encoder = JSONEncoder()
        self.assertEqual(encoder.encode(test_obj), json.dumps(test_obj))

    def test_empty(self):
        test_obj = {}
        encoder = JSONEncoder()
        self.assertEqual(encoder.encode(test_obj), json.dumps(test_obj))

    def test_list(self):
        test_obj = [i for i in range(10)]
        encoder = JSONEncoder()
        self.assertEqual(encoder.encode(test_obj), json.dumps(test_obj))

    def test_simple_dict(self):
        test_obj = {'hello': 'world'}
        encoder = JSONEncoder()
        self.assertEqual(encoder.encode(test_obj), json.dumps(test_obj))

    def test_constant(self):
        test_obj = {'null': None, 'inf': float('inf'), '-inf': float('-inf'),
                    'false': False, 'true': True}
        encoder = JSONEncoder()
        self.assertEqual(encoder.encode(test_obj), json.dumps(test_obj))

    def test_nested_dict(self):
        test_obj = {"outer": {"inner": [{"x": 1.0, "y": 2.2}, {"x": 2.0, "y": 4.2}]}}
        encoder = JSONEncoder()
        self.assertEqual(encoder.encode(test_obj), json.dumps(test_obj))

    def test_no_string_key(self):
        test_obj = {(1, 2, 3): 'world'}
        encoder = JSONEncoder()
        with self.assertRaises(KeyError):
            encoder.encode(test_obj)


class TestJSONParser(unittest.TestCase):
    def setUp(self):
        print('---------- Setup file -------------')
        self.test_obj = {'a': [1, 2, 3, 4, 5, (6, 7), '123']}
        self.file_path = 'test.json'
        with open(self.file_path, 'w+') as f:
            f.write(json.dumps(self.test_obj))

    def tearDown(self):
        try:
            os.remove('test.json')
        except OSError:
            pass

    def test_load_file(self):
        parser = JSONParser()
        parser.load_file(self.file_path)
        with open(self.file_path) as f:
            self.assertDictEqual(parser.dump_dict(), json.loads(f.read()))

    def test_dump_file(self):
        parser = JSONParser()
        os.remove('test.json')
        parser.dump_file(self.file_path)
        with open(self.file_path, 'r') as file:
            c = file.read()
        with open(self.file_path, 'r') as file:
            self.assertEqual(c, json.dumps(json.load(file)))
# TODO add large number, UNICODE to test

if __name__ == '__main__':
    unittest.main()
