"""Contactbook global variables
"""
import os
import sys
try:
    from utils.settings import config
    from helpers.datahelper import TypeEnum
    from errors import exceptions
except ModuleNotFoundError:
    from .utils.settings import config
    from .helpers.datahelper import TypeEnum, JsonHelper, ConditionEnum
    from .errors import exceptions

sys.path.append(os.path.dirname(os.path.realpath(__file__)))
DATA_PATH = os.path.join(os.path.dirname(__file__), config['data']['file_path'])
SCHEMA_PATH = os.path.join(os.path.dirname(__file__), config['data']['schema_path'])
helper = JsonHelper(source=DATA_PATH, schema=SCHEMA_PATH)
OUTPUT_FORMAT = None
if config['data']['output_format'] == 'namedtuple':
    OUTPUT_FORMAT = TypeEnum.NAMEDTUPLE
elif config['data']['output_format'] == 'dictionary':
    OUTPUT_FORMAT = TypeEnum.DICTIONARY
else:
    msg = 'Type not in our supported list'
    raise exceptions.NotSupportedTypeError(msg)

__all__ = ['DATA_PATH', 'SCHEMA_PATH', 'OUTPUT_FORMAT', 'helper']
