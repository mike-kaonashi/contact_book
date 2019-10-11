"""Contactbook global variables
"""
import os

try:
    from .utils.settings import config
    from .helpers.datahelper import TypeEnum
except ModuleNotFoundError:
    from utils.settings import config
    from helpers.datahelper import TypeEnum

DATA_PATH = os.path.join(os.path.dirname(__file__), config['data']['file_path'])
SCHEMA_PATH = os.path.join(os.path.dirname(__file__), config['data']['schema_path'])
OUTPUT_FORMAT = None
if config['data']['output_format'] == 'namedtuple':
    OUTPUT_FORMAT = TypeEnum.NAMEDTUPLE
elif config['data']['output_format'] == 'dictionary':
    OUTPUT_FORMAT = TypeEnum.DICTIONARY

__all__ = ['DATA_PATH', 'SCHEMA_PATH', 'OUTPUT_FORMAT']
