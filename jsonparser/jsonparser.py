# vim: set et ts=4 sw=4
# coding: utf8
# !/usr/bin/python

from .decoder import JSONDecoder
from .encoder import JSONEncoder


class JSONParser(object):
    """
    A Json Parser, which can load and dump from either file or dict
    Reference: http://json.org/json-zh.html
    """

    def __init__(self):
        self._data = {}
        self.decoder = JSONDecoder()
        self.encoder = JSONEncoder()

    def __getitem__(self, key):
        return self._data[key]

    def __setitem__(self, key, value):
        self._data.__setitem__(key,value)

    def __delitem__(self, key):
        self._data.__delitem__(key)

    def loads(self, s):
        """
        load and decode from string
        :param s: JSON string
        :return: None
        """
        self._data = self.decoder.decode(s)

    def dumps(self):
        """
        Decode the object
        :return: JSON string
        """
        return self.encoder.encode(self._data)

    def load_file(self, path):
        """
        Load the json from file
        :param path:
        :return: None
        """
        with open(path, 'r') as f:
            s = f.read()
            self.loads(s)

    def dump_file(self, path):
        """
        Save the JSON object to file
        :param path:
        :return: None
        """
        with open(path, 'w+') as f:
            f.write(self.dumps())

    def load_dict(self, input_dict):
        """
        Make a deep copy of parameter
        :param input_dict:
        :return: None
        """
        self._data = dict(input_dict)

    def dump_dict(self):
        """
        Return saved JSON Object
        :return:
        """
        return dict(self._data)

    def update(self, *others):
        """
        Update the dict with new given dict
        :param others:
        :return:
        """
        self._data.update(others)
