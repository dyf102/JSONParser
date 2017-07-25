# vim: set et ts=4 sw=4
# coding: utf8
# !/usr/bin/python

import json
import jsonparser
import logging
from jsonparser import InvalidJSONStringFormatException

json_ok = [
    ('{}', 1),
    ('{"":""}', 1),
    ('{"a":123}', 1),
    ('{"a":-123}', 1),
    ('{"a":1.23}', 1),
    ('{"a":1e1}', 1),
    ('{"a":true,"b":false}', 1),
    ('{"a":null}', 1),
    ('{"a":[]}', 1),
    ('{"a":{}}', 1),
    (' {"a:": 123}', 1),
    ('{ "a  " : 123}', 1),
    ('{ "a" : 123        }', 1),
    ('{"true": "null"}', 1),
    ('{"":"\\t\\n"}', 1),
    ('{"\\"":"\\""}', 1),
]

json_ok2 = [
    ('{"a":"abcde,:-+{}[]"}', 2),
    ('{"a": [1,2,"abc"]}', 2),
    ('{"d{": "}dd", "a":123}', 2),
    ('{"a": {"a": {"a": 123}}}', 2),
    ('{"a": {"a": {"a": [1,2,[3]]}}}', 2),
    ('{"a": "\\u7f51\\u6613CC\\"\'"}', 3),

    ('{"a":1e-1, "cc": -123.4}', 2),
    ('{ "{ab" : "}123", "\\\\a[": "]\\\\"}', 3), ]

json_ex = [
    # exceptions
    ('{"a":[}', 2),
    ('{"a":"}', 2),

    ('{"a":True}', 1),
    ('{"a":Null}', 1),
    ('{"a":foobar}', 2),
    ("{'a':1}", 3),
    ('{1:1}', 2),
    ('{true:1}', 2),
    ('{"a":{}', 2),
    ('{"a":-}', 1),
    ('{"a":[,]}', 2),
    ('{"a":.1}', 1),
    ('{"a":+123}', 1),
    ('{"a":1..1}', 1),
    ('{"a":--1}', 1),
    ('{"a":"""}', 1),
    ('{"a":"\\"}', 1),
]


def test_ok_1():
    print('Test OK 1')
    print('-' * 50)
    for (test, ptr) in json_ok:
        #try:
        jsonparser.loads(test)
        #except Exception as e:
        #    logging.warning('%s', test)
        #    raise e
        #    break
        c = json.loads(test)
        if c != jsonparser.dump_dict():
            print(c)
            print(jsonparser.dump_dict())
        else:
            print('Passed')


def test_ok_2():
    print('Test OK 2')
    print('-' * 50)
    for (test, ptr) in json_ok2:
        try:
            jsonparser.loads(test)
        except Exception as e:
            logging.warning('%s', test)
            raise e
            break
        c = json.loads(test)
        if c != jsonparser.dump_dict():
            print(c)
            print(jsonparser.dump_dict())
        else:
            print('Passed')


def test_ex():
    print('Test Exception Case')
    print('-' * 50)
    for (test, ptr) in json_ex:
        try:
            jsonparser.loads(test)
        except InvalidJSONStringFormatException as e:
            print('Passed')
            pass
        else:
            logging.warning('%s', test)
            break

if __name__ == "__main__":
    test_ok_1()
    test_ok_2()
    test_ex()
