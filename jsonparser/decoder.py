# vim: set et ts=4 sw=4
# coding: utf8
# !/usr/bin/python
import re
import logging

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


class InvalidJSONStringFormatException(Exception):
    def __init__(self, msg):
        self.msg = msg

    def __str__(self):
        return 'Invalid JSON string format Exception: {}'.format(self.msg)


class JSONDecoder(object):

    def __init__(self):
        self._str = None
        self._idx = 0
        self._ch = None

    def decode(self, s):
        if not isinstance(s, str):
            raise TypeError('expected string')
        if len(s) == 0:
            raise ValueError('No JSON object could be decoded')
        self._idx = 0
        self._str = s
        self._ch = s[0]
        self._parse_white_space()
        return self._parse_obj()

    def _parse_obj(self):
        if self._ch != '{':
            raise AssertionError()
        self._next()
        dic = {}
        if self._ch == '}':
            return {}  # handle empty object
        while True:
            self._parse_white_space()  # skip
            if self._ch != '"':
                raise InvalidJSONStringFormatException('Object Key must be a string')
            key = self._parse_string()
            self._parse_white_space()
            if self._ch not in ':':
                raise InvalidJSONStringFormatException('Expect colon')
            self._next()  # to skip ':'
            self._parse_white_space()
            value = self._parse_value()
            self._parse_white_space()
            dic[key] = value
            if self._ch == '}':  # end of object
                self._next()
                break
            elif self._ch == ',':
                self._next()
                continue
            else:
                raise InvalidJSONStringFormatException('Expect commas')
        return dic

    def _next(self, step=1):
        """
        Move to next position
        @:param step, default = 1
        @:except InvalidJSONStringFormatException
        """
        self._idx += step
        if self._idx < len(self._str):
            self._ch = self._str[self._idx]
        else:
            raise InvalidJSONStringFormatException('Unexpected string')

    def _has_next(self):
        return self._idx <= len(self._str)

    def _get_remain(self):
        return self._str[self._idx:]

    def _parse_null(self):
        """
        :return None if invalid string:
        :return s: Return a copy of the string with null removed
        """
        if self._get_remain().startswith('null'):
            self._next(4)  # move 4 steps
            return None
        else:
            raise InvalidJSONStringFormatException()

    def _parse_white_space(self):
        """
        :return s: Return a copy of the string with escape characters removed
        """
        while self._ch in _ESCAPE_LIST and self._has_next():
            self._next()

    def _parse_list(self):
        if self._ch != '[':
            raise AssertionError()
        self._next()
        li = []
        while self._has_next() and self._ch != ']':
            if self._ch != ',':
                li.append(self._parse_value())
                if self._ch == ']':
                    break
                self._next()
            else:
                raise InvalidJSONStringFormatException('unknown delimiter {}'.format(self._ch))
        if self._ch == ']':
            self._next()
            return li
        else:
            raise InvalidJSONStringFormatException('expected {}'.format(']'))

    def _parse_string(self):
        if self._ch != '"':
            raise AssertionError()
        self._next()
        chunks = []
        _append = chunks.append
        # TODO: add Unicode support
        while self._has_next():
            ch = self._ch
            if ch == '"':
                self._next()
                return u''.join(chunks)
            elif ch == '\\':  # TODO: add \u
                self._next()
                if self._ch in ESCAPE.keys():
                    _append(ESCAPE[self._ch])
                elif self._ch == 'u':
                    _append(unichr(self._decode_unicode()))
                    self._next(4)
            else:
                _append(ch)
            self._next()
        raise InvalidJSONStringFormatException('Missing closure \" ')

    def _parse_boolean(self):
        if self._get_remain().startswith('true'):
            self._next(4)
            return True
        elif self._get_remain().startswith('false'):
            self._next(5)
            return False
        else:
            raise InvalidJSONStringFormatException('Invalid constant')

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
        else:
            raise InvalidJSONStringFormatException('Unexpected Token')

    def _parse_value(self):
        self._parse_white_space()
        if self._ch == '{':
            return self._parse_obj()
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
                msg = 'Exception Occurs at pos:{}'.format(self._idx)
                raise InvalidJSONStringFormatException(msg)

    def _decode_unicode(self):
        pos = self._idx
        esc = self._str[pos + 1:pos + 5]
        if len(esc) == 4 and esc[1] not in 'xX':
            try:
                return int(esc, 16)
            except ValueError:
                pass
        msg = "Invalid \\uXXXX escape"
        raise ValueError(msg)
