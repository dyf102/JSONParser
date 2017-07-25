# vim: set et ts=4 sw=4
# coding: utf8
# !/usr/bin/python
__version__ = '0.1'
__all__ = [
    'dumps', 'loads',
    'JSONDecoder', 'JSONEncoder',
    'dump_file', 'load_file',
    'load_dict', 'dump_dict'
]
__author__ = 'Yuwei Duan<dyf102@gmail.com>'

from .jsonparser import JSONParser

parser  = JSONParser()

def loads(s):
    return parser.loads(s)

def dumps():
    return parser.dumps()

def dump_dict(input_dict):
    return parser.dump_dict

def load_dict(self, input_dict):
    return parser.load_dict(input_dict)

def dump_file(path):
    return parser.dump_file(path)

def load_file(path):
    return parser.load_file(path)

def update(*others):
    return parser.update(others)

