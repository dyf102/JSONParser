# vim: set et ts=4 sw=4
# coding: utf8
# !/usr/bin/python

ESCAPE_DCT = {
    '\\': '\\\\',
    '"': '\\"',
    '\b': '\\b',
    '\f': '\\f',
    '\n': '\\n',
    '\r': '\\r',
    '\t': '\\t',
}
CONST_DCT = {
	True: 'true',
	False: 'False',
	None: 'null',
	float('inf'): 'infinity',
	float('-inf'): '-infinity'
}
class JSONEncoder(object):
"""
	Extensible JSON <http://json.org> encoder for Python data structures.
    Supports the following objects and types by default:
    +-------------------+---------------+
    | Python            | JSON          |
    +===================+===============+
    | dict, namedtuple  | object        |
    +-------------------+---------------+
    | list, tuple       | array         |
    +-------------------+---------------+
    | str, unicode      | string        |
    +-------------------+---------------+
    | int, long, float  | number        |
    +-------------------+---------------+
    | True              | true          |
    +-------------------+---------------+
    | False             | false         |
    +-------------------+---------------+
    | None              | null          |
    +-------------------+---------------+
"""
    def __init__(self):
        self.str_list = []


    def _encode_str(self, str):
    	return unicode(str)

    def _encode_dict(self, dict):
    	str_list = ['{']
    	_append = str_list.append
    	is_first = True
    	for k, v in dict.items():
    		if not isinstance(k, str):
    			raise KeyError('keys must be a string')
    		if not is_first:
    			_append(',')
    		_append(k)
    		_append(':')
    		_append(self.encode(v))
    		is_first = False
    	_append('}')
    	return ''.join(str_list)

    def _encode_constant(self, c):
    	try:
    		c_str = CONST_DCT[c]
    		return c_str
    	except KeyError:
    		raise AssertionError()
    
    def _encode_int_float(self, num):
    	return str(num)
    
    def _encode_list(self, items):
    	str_list = ['[']
    	_append = str_list.append()
    	is_first = True
    	for item in items:
    		if not is_first:
    			_append(',')
    		_append(self.encode(item))
    	_append(']')
    	return ''.join(str_list)
    def _encode_str(self, s):
    	return s
    
    def encode(self, obj):
        """
        :param dict:
        :return:
        """
        if isinstance(obj, str):
        	return self._encode_str(str)
        elif isinstance(obj, dict):
        	return self._encode_dict(obj)
        elif isinstance(obj, list) or 
        	isinstance(obj, tuple):
        	return self._encode_list(obj)
        return ''.join(self.str_list)
