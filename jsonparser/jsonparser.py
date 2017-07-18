# vim: set et ts=4 sw=4
# coding: utf8
# !/usr/bin/python

# STRING_SPLIT = re.compile(r'(.*?)(["\\\x00-\x1f])',
#    (re.VERBOSE | re.MULTILINE | re.DOTALL))
from .decoder import JSONDecoder
from .encoder import JSONEncoder



class JSONParser(dict):
    """
    A Json Parser, which can load and dump from either file or dict
    Reference: http://json.org/json-zh.html
    """

    def __init__(self):
        super.__init__(self)
        self._data = {}
        pass

    def __getitem__(self, key):
        return self._data[key]

    def __setitem__(self, key, value):
        self._data.__setitem__(key,value)

    def __delitem__(self, key):
        self._data.__delitem__(key)

    def loads(self, s):
        pass

    def dumps(self):
        """
        :return:
        """
        pass

    def load_file(self, f):
        pass

    def dump_file(self, f):
        pass

    def load_dict(self, dict):
        pass

    def dump_dict(self):
        pass

    def update(self, *others):
        self._data.update(others)



