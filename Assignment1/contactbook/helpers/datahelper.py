import os
import sys
import json
import time
import logging
from datetime import datetime
import collections
from enum import Enum
try:
    from errors import exceptions
    from validator import Validator
    from caster import Caster
except ModuleNotFoundError:
    from ..errors import exceptions
    from .validator import Validator

_now = datetime.now()
_today = datetime(_now.year, _now.month, _now.day)
_log_file = '{today}_record.log'.format(today=int(time.mktime(_today.timetuple())))
_root_dir = os.path.join(os.path.dirname(sys.modules['__main__'].__file__), 'logs')
_log_path = os.path.join(_root_dir, _log_file)
if not os.path.exists(_root_dir):
    os.makedirs(_root_dir)
logging.basicConfig(filename=_log_path, filemode='a+', level=logging.INFO,
                    format='%(asctime)s-%(levelname)s %(filename)s:%(lineno)s  %(message)s')


class TypeEnum(Enum):
    DICTIONARY = 0
    NAMEDTUPLE = 1
    NOTDEFINED = -1


class ConditionEnum(Enum):
    EQUAL = '='
    GREATER = '>'
    GREATER_EQUAL = '>='
    LESSER = '<'
    LESSER_EQUAL = '<='


class DataHelper:
    def __init__(self, source=None):
        super()
        self._data_source = source
        self.validator = Validator()

    def read_data(self, type_):
        msg = '.read_data() need to be override'
        raise NotImplementedError(msg)

    def write_data(self, target):
        msg = '.write_data() need to be override'
        raise NotImplementedError(msg)


class JsonHelper(DataHelper):
    """Help to parse, convert data in json format
    """

    def __init__(self, source=None, schema=None):
        super().__init__(source)
        self._schema = None
        if schema:
            try:
                raw_ = open(schema, 'r')
                self._schema = json.loads(raw_.read())
            except (FileExistsError, FileNotFoundError):
                msg = 'File does not exist or not found'
                logging.error(msg)
                raise exceptions.NotAvailableFileError(msg)

    @property
    def _headers(self):
        return [item['name'].lower() for item in self._schema['fields']]

    def read_data(self, type_=TypeEnum.DICTIONARY):
        """Read data from target file and parse to python readable data
        :param type_: Convert data from json into pre-defined type
        :return:
        """
        logging.info('Start reading data from file...')
        try:
            source_ = open(self._data_source, 'r')
        except (FileExistsError, FileNotFoundError):
            msg = 'File does not exist or not found'
            logging.error(msg)
            raise exceptions.NotAvailableFileError(msg)
        try:
            results = json.load(source_)
        except json.decoder.JSONDecodeError:
            msg = 'The file not in Json format or empty file'
            logging.error(msg)
            raise TypeError(msg)
        try:
            print('Here')
            if TypeEnum.DICTIONARY.__eq__(type_.value):
                results = [self.apply_schema(item) for item in results]
            elif TypeEnum.NAMEDTUPLE.__eq__(type_.value):
                Object = collections.namedtuple('Object', self._headers)
                results = [self.apply_schema(Object._make(item.values())) for item in results]

        except Exception:
            msg = 'The data does not fit with the pre-defined schema.'
            logging.error('Data does not fit the schema.')
            raise exceptions.NotFitSchemaError(msg)
        source_.close()
        logging.info('Done reading data.')
        return results

    def write_data(self, target):
        """Cast all properties of data into string format
        Then write it to target json file
        :param target: input data
        :return:
        """
        list_ = self.read_data(type_=TypeEnum.NOTDEFINED)
        logging.info('Start writing data to the file...')
        if len(self._headers) != len(target):
            msg = 'The data does not fit the schema.'
            logging.error(msg)
            raise exceptions.NotFitSchemaError(msg)
        else:
            tmp = dict(zip(self._headers, [item for item in target]))
            if self.validator.check_obj_by_schema(tmp, self._schema):
                target_ = dict(zip(self._headers, [str(item) for item in target]))
                list_.append(target_)
            else:
                msg = 'The data does not fit the schema.'
                logging.error(msg)
                raise exceptions.NotFitSchemaError(msg)
            try:
                source_ = open(self._data_source, mode='w')
                json.dump(list_, source_, indent=4)
                source_.close()
            except (FileExistsError, FileNotFoundError):
                msg = 'The file does not exist or not found'
                logging.error(msg)
                raise exceptions.NotAvailableFileError(msg)
        logging.info('Done writing data to the file.')
        return target_

    def apply_schema(self, target_unit):
        """Apply data schema for target obj (only for flatten data)
        :param target_unit: Object on casting mode to fit the schema
        :return:
        """
        data_caster = Caster()
        
        for field in self._schema['fields']:
            if field['metadata']:
                data_caster.set_metadata(field['metadata'])
            else:
                data_caster.set_metadata(None)
            target_unit = data_caster.cast_type(field, target_unit)
        return target_unit

    def filter_data(self, target, field_name, keyword=None, mode_list=None):
        """ Help to filter data with user's input conditions
        :param target: Input list objects
        :param field_name: Selected field to filter
        :param keyword: Keyword to filter on specific field
        :param mode_list: Mode condition for range filter
        :return:
        """
        logging.info('Start filtering data...')
        if field_name not in self._headers:
            msg = "Field name does not exist in the headers"
            logging.error(msg)
            raise exceptions.NotExistFieldNameError(msg)
        if mode_list is None:
            target = [item for item in target if keyword in self.validator.get_attr_with_format(item, field_name)]
        elif len(mode_list) == 0:
            msg = 'Nothing to filter.'
            logging.warning(msg)
            target = []
        else:
            for item in mode_list:
                # Validate input data for age field
                if not isinstance(item['value'], int):
                    msg = 'Input value must be in Integer format.'
                    logging.error(msg)
                    raise exceptions.NotAvailableValueError(msg)
                if item['value'] < 0:
                    msg = 'Input value must be positive number'
                    logging.error(msg)
                    raise exceptions.NotAvailableValueError(msg)
                # Filter data every single mode in list.
                if ConditionEnum.EQUAL.__eq__(item['mode']):
                    target = [i for i in target if self.validator.get_attr_with_format(i, field_name) == item['value']]
                elif ConditionEnum.LESSER.__eq__(item['mode']):
                    target = [i for i in target if self.validator.get_attr_with_format(i, field_name) < item['value']]
                elif ConditionEnum.LESSER_EQUAL.__eq__(item['mode']):
                    target = [i for i in target if self.validator.get_attr_with_format(i, field_name) <= item['value']]
                elif ConditionEnum.GREATER.__eq__(item['mode']):
                    target = [i for i in target if self.validator.get_attr_with_format(i, field_name) > item['value']]
                elif ConditionEnum.GREATER_EQUAL.__eq__(item['mode']):
                    target = [i for i in target if self.validator.get_attr_with_format(i, field_name) >= item['value']]
        logging.info('Done filtering data.')
        return target if len(target) > 0 else None
