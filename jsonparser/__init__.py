__version__ = '0.1'
__all__ = [
    'dumps', 'loads',
    'JSONDecoder', 'JSONEncoder',
    'dump_file', 'load_file',
    'load_dict', 'dump_dict'
]
__author__ = 'Yuwei Duan<dyf102@gmail.com>'

from .decoder import JSONDecoder
from .encoder import JSONEncoder
