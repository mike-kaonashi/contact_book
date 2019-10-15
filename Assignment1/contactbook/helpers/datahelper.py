import os
import sys
import json
import time
import logging
import datetime
import collections
from enum import Enum
try:
    from errors import exceptions
except ModuleNotFoundError:
    from ..errors import exceptions

_now = datetime.datetime.now()
_today = datetime.datetime(_now.year, _now.month, _now.day)
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
        if schema is not None:
            try:
                raw_ = open(schema, 'r')
                self._schema = json.loads(raw_.read())
            except (FileExistsError, FileNotFoundError):
                raise exceptions.NotAvailableFileError

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
            if type_.value == TypeEnum.DICTIONARY.value:
                results = [self.apply_schema(item) for item in results]
            elif type_.value == TypeEnum.NAMEDTUPLE.value:
                Object = collections.namedtuple('Object', self._headers)
                results = [self.apply_schema(Object._make(item.values())) for item in results]

        except Exception:
            msg = 'The data does not fit with the pre-defined schema.'
            logging.error('Data does not fit the schema.')
            raise exceptions.NotFitSchemaError(msg)
        logging.info('Done reading data.')
        source_.close()
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
            target_ = dict(zip(self._headers, [str(item) for item in target]))
            list_.append(target_)
            try:
                source_ = open(self._data_source, mode='w')
            except (FileExistsError, FileNotFoundError):
                msg = 'The file does not exist or not found'
                logging.error(msg)
                raise exceptions.NotAvailableFileError(msg)
            json.dump(list_, source_, indent=4)
            source_.close()
        logging.info('Done writing data to the file.')
        return target_

    def apply_schema(self, target_unit):
        """Apply data schema for target obj (only for flatten data)
        :param target_unit: Object on casting mode to fit the schema
        :return:
        """
        def cast_dict(unit, prop_name, prop_value, prop_type, metadata=None):
            if prop_type == "string":
                unit[prop_name] = str(prop_value)
            elif prop_type == "integer":
                unit[prop_name] = int(prop_value)
            elif prop_type == "float":
                unit[prop_name] = float(prop_value)
            elif prop_type == "date":
                date_format = metadata['date_format']
                unit[prop_name] = datetime.datetime.strptime(prop_value, date_format)

        def cast_tuple(unit, prop_name, prop_value, prop_type, metadata=None):
            if prop_type == "string":
                unit = unit._replace(**{prop_name: str(prop_value)})
            elif prop_type == "integer":
                unit = unit._replace(**{prop_name: int(prop_value)})
            elif prop_type == "float":
                unit = unit._replace(**{prop_name: float(prop_value)})
            elif prop_type == "date":
                date_format = metadata['date_format']
                unit = unit._replace(**{prop_name: datetime.datetime.strptime(prop_value, date_format)})
            return unit

        def cast_type(field_props, unit):
            current_value = None
            if isinstance(unit, dict):
                current_value = unit[field_props['name'].lower()]
            elif isinstance(unit, tuple):
                current_value = getattr(unit, field_props['name'].lower())
            if field_props['nullable'] is False \
                    and current_value is None:
                msg = 'Field property must be not null.'
                logging.error(msg)
                raise TypeError(msg)
            try:
                current_type = field_props['type']
                current_name = field_props['name'].lower()
                if isinstance(unit, dict):
                    cast_dict(unit, current_name, current_value, current_type, field_props['metadata'])
                elif isinstance(unit, tuple):
                    unit = cast_tuple(unit, current_name, current_value, current_type, field_props['metadata'])
            except ValueError:
                logging.error('Can not define the type of the agent.')
                raise ValueError('Undefined type of property')
            return unit

        for field in self._schema['fields']:
            target_unit = cast_type(field, target_unit)
        return target_unit

    @staticmethod
    def filter_data(target, field_name, keyword=None, mode_list=None, output_format=None):
        """ Help to filter data with user's input conditions
        :param target: Input list objects
        :param field_name: Selected field to filter
        :param keyword: Keyword to filter on specific field
        :param mode_list: Mode condition for range filter
        :param output_format: Format of output data
        :return:
        """
        logging.info('Start filtering data...')

        def get_attr_with_format(item, field, format_):
            if format_.value == TypeEnum.DICTIONARY.value:
                return item[field]
            elif format_.value == TypeEnum.NAMEDTUPLE.value:
                return getattr(item, field)

        if mode_list is None:
            target = [item for item in target if keyword in get_attr_with_format(item, field_name, output_format)]
        elif len(mode_list) == 0:
            msg = 'Nothing to filter.'
            logging.warning(msg)
            return None
        else:
            for item in mode_list:
                if not isinstance(item['value'], int):
                    msg = 'Input value must be in Integer format.'
                    logging.error(msg)
                    raise exceptions.NotAvailableValueError(msg)
                if item['value'] < 0:
                    msg = 'Input value must be positive number'
                    logging.error(msg)
                    raise exceptions.NotAvailableValueError(msg)
                if item['mode'] == ConditionEnum.EQUAL.value:
                    target = [i for i in target if get_attr_with_format(i, field_name, output_format) == item['value']]
                elif item['mode'] == ConditionEnum.LESSER.value:
                    target = [i for i in target if get_attr_with_format(i, field_name, output_format) < item['value']]
                elif item['mode'] == ConditionEnum.LESSER_EQUAL.value:
                    target = [i for i in target if get_attr_with_format(i, field_name, output_format) <= item['value']]
                elif item['mode'] == ConditionEnum.GREATER.value:
                    target = [i for i in target if get_attr_with_format(i, field_name, output_format) > item['value']]
                elif item['mode'] == ConditionEnum.GREATER_EQUAL.value:
                    target = [i for i in target if get_attr_with_format(i, field_name, output_format) >= item['value']]
        logging.info('Done filtering data.')
        return target
