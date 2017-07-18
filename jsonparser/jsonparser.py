# vim: set et ts=4 sw=4
# coding: utf8
# !/usr/bin/python
import re

_ESCAPE_LIST = ['\n', '\t', '\r', ' ']
ESCAPE = {
    'b': '\b',
    'n': '\n',
    't': '\t',
    'r': '\r',
    'f': '\f',
    '\"': '\"',
    '\\': '\\'
}
NUMBER_RE = re.compile(
    r'(-?(?:0|[1-9]\d*))(\.\d+)?([eE][-+]?\d+)?',
    (re.VERBOSE | re.MULTILINE | re.DOTALL))
# STRING_SPLIT = re.compile(r'(.*?)(["\\\x00-\x1f])',
#    (re.VERBOSE | re.MULTILINE | re.DOTALL))


class InvalidJSONStringFormatException(Exception):
    def __str__(self):
        return 'Invalid Input Exception'


class JSONParser(object):
    """
    A Json Parser, which can load and dump from either file or dict
    Reference: http://json.org/json-zh.html
    """

    def __init__(self):
        self._data = {}
        self._str = None
        self._idx = 0
        self._ch = None

    def loads(self, s):
        """
        :param s, a JSON string
        :return: None
        """
        if not isinstance(s, str):
            return None
        self._idx = 0
        self._str = s
        self._ch = s[0]
        #self._data = self._parse_value()

    def parse_obj(self):
        if self._ch != '{':
            raise AssertionError()
        self._next()
        key = self._parse_string()
        if self._ch != ':':
            raise InvalidJSONStringFormatException()
        value = self._parse_value()

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

    def _next(self, step=1):
        """
        Move to next position
        """
        self._idx += step
        self._ch = self._str[self._idx]

    def _has_next(self):
        return self._idx <= len(self._str)

    def _get_remain(self):
        return self._str[self._idx:]

    def _parse_null(self):
        """
        :return None if invalid string:
        :return s: Return a copy of the string with null removed
        """
        if self._str.startswith('null'):
            self._next(4)  # move 4 steps
            return None
        else:
            raise InvalidJSONStringFormatException()

    def _parse_white_space(self):
        """
        :return s: Return a copy of the string with escape characters removed
        """
        while self._ch in _ESCAPE_LIST:
            self._next()

    def _parse_list(self):
        li = []
        if self._ch != '[':
            raise AssertionError()
        while self._has_next() and self._ch != ']':
            if self._ch != ',':
                li.append(self._parse_value())
            self._next()
        if self._ch == ']':
            return li
        else:
            raise InvalidJSONStringFormatException()

    def _parse_string(self):
        if self._ch != '"':
            raise InvalidJSONStringFormatException()
        # print(self._get_remain(), self._idx)
        self._next()
        chunks = []
        _append = chunks.append
        #_m = STRING_SPLIT.match
        # TODO: add Unicode support
        while self._has_next():
            ch = self._ch
            if ch == '"':
                return u''.join(chunks)
            elif ch == '\\':  # TODO: add \u
                self._next()
                if self._ch in ESCAPE.keys():
                    _append(ESCAPE[self._ch])
            else:
                _append(ch)
            self._next()
        raise InvalidJSONStringFormatException()

    def _parse_boolean(self):
        if self._get_remain().startswith('true'):
            self._next(4)
            return True
        elif self._get_remain().startswith('false'):
            self._next(5)
            return False
        else:
            raise InvalidJSONStringFormatException()

    def _parse_number(self):
        number_match = NUMBER_RE.match
        m = number_match(self._get_remain(), 0)
        if m is not None:
            integer, frac, exp = m.groups()
            if frac or exp:
                res = float(integer + (frac or '') + (exp or ''))
            else:
                res = int(integer)
            return res, m.end()
        elif self._ch == 'N' and self._get_remain().startswith('NaN'):
            return float('nan'), 3
        elif self._ch == 'I' and self._get_remain().startswith('Infinity'):
            return float('inf'), 8
        elif self._ch == '-' and self._get_remain().startswith('-Infinity'):
            return float('-inf'), 9

    def _parse_value(self):
        self._parse_white_space()
        if self._ch == '{':
            return self.parse_obj()
        elif self._ch == '[':
            return self._parse_list()
        elif self._ch in ('f', 't'):
            return self._parse_boolean()
        elif self._ch == 'n':
            return self._parse_null()
        elif self._ch == '"':
            return self._parse_string()
        else:
            if self._ch == '-' or (str(self._ch)).isdigit():
                (number, step) = self._parse_number()
                self._next(step)
                return number
            else:
                raise InvalidJSONStringFormatException()
if __name__ == "__main__":
    test_string_1 = '"Altitude"'
    test_string_2 = '""'
    test_number_1 = '123' #123
    test_number_2 = '-123' #-123
    test_number_3 = '3.1415' #3.1415
    test_number_4 = '10e100' #10e100
    test_number_5 = '10e10000' #inf
    test_number_6 = '-10e10000' #-inf
    parser = JSONParser()
    parser.loads(test_number_6)
    print(parser._parse_number())
