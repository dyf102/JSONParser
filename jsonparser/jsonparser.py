# vim: set et ts=4 sw=4
# coding: utf8
# !/usr/bin/python


_ESCAPE_LIST = ['\n', '\t', '\r', ' ']

class JSONObj(dict):

    def __repr__(self):
        return dict.__str__()

class InvalidJSONStringFormatException(Exception):
    def __str__(self):
        return 'Invalid Input Exception'

class JSONParser(object):
    """
    A Json Parser, which can load and dump from either file or dict
    Reference: http://json.org/json-zh.html
    """

    def __init__(self):
        self._data = JSONObj()

    def loads(self, s):
        """
        :param s, a JSON string
        :return: None
        """
        if not isinstance(s):
            return None
        idx = 0
        pass

    def load(self, idx, s):
        total_len = len(s)
        if idx == total_len:
            return
        c = s[idx]
        if c == '{':
           self.parse_obj(idx + 1, s)
    def parse_obj(self, s, v):
        if not isinstance(s, str):
            return None
        if s[0] != '{': raise InvalidJSONStringFormatException()
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

    def get_data(self):
        return self._data

    @staticmethod
    def _parse_null(s):
        """
        :param s:
        :return None if invalid string:
        :return s: Return a copy of the string with null removed
        """
        if not isinstance(s, str):
            return None
        if not s.startswith('null'):
            return None
        return s[4:]

    @staticmethod
    def _parse_white_space(s):
        """
        :param s: JSON string
        :return s: Return a copy of the string with escape characters removed
        """
        if not isinstance(s, str):
            return None
        return s.lstrip(_ESCAPE_LIST)

    @staticmethod
    def _parse_value(s):
        pass
if __name__ == "__main__":
    test_case_1 = '{"Altitude" : -1.123}'
    print(JSONParser.get_data())
