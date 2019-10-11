import json
import datetime
import collections
from enum import Enum


class NotFitSchemaError(Exception):
    """The data doesn't fit with the pre-defined schema.
    """
    pass


class FileNotAvailableError(Exception):
    """File does not exist or can't be found.
    """
    pass


class NotInJsonFormatError(Exception):
    """File not in Json format for parsing stuffs
    """
    pass


class NullFilterConditionError(Exception):
    """Null params for filtering stuffs
    """
    pass


class TypeNotSupportedException(Exception):
    """Type not in our supported list
    """
    pass


class TypeEnum(Enum):
    DICTIONARY = 0
    NAMEDTUPLE = 1


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
        raise NotImplementedError

    def write_data(self, target):
        raise NotImplementedError


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
                raise FileNotAvailableException

    @property
    def _headers(self):
        return [item['name'].lower() for item in self._schema['fields']]

    def read_data(self, type_=TypeEnum.DICTIONARY):
        """Read data from target file and parse to python readable data
        :param type_: Convert data from json into pre-defined type
        :return:
        """
        try:
            source_ = open(self._data_source, 'r')
        except (FileExistsError, FileNotFoundError):
            raise FileNotAvailableError
        try:
            results = json.load(source_)
        except json.decoder.JSONDecodeError:
            raise TypeError
        try:
            if type_ is TypeEnum.DICTIONARY:
                results = [self.apply_schema(item) for item in results]
            elif type_ is TypeEnum.NAMEDTUPLE:
                Object = collections.namedtuple('Object', self._headers)
                results = [self.apply_schema(Object._make(item.values())) for item in results]
        except Exception:
            raise NotFitSchemaError
        source_.close()
        return results

    def write_data(self, target):
        """Cast all properties of data into string format
        Then write it to target json file
        :param target: input data
        :return:
        """
        list_ = self.read_data()
        try:
            source_ = open(self._data_source, mode='w')
        except (FileExistsError, FileNotFoundError):
            raise FileNotAvailableException
        if len(self._headers) != len(target):
            raise NotFitSchemaException
        target_ = dict(zip(self._headers, [str(item) for item in target]))
        list_.append(target_)
        json.dump(list_, source_, indent=4)
        source_.close()
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
                raise TypeError
            try:
                current_type = field_props['type']
                current_name = field_props['name'].lower()
                if isinstance(unit, dict):
                    cast_dict(unit, current_name, current_value, current_type, field_props['metadata'])
                elif isinstance(unit, tuple):
                    unit = cast_tuple(unit, current_name, current_value, current_type, field_props['metadata'])
            except ValueError:
                raise ValueError
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

        def get_attr_with_format(item, field, format_):
            if format_ is TypeEnum.DICTIONARY:
                return item[field]
            elif format_ is TypeEnum.NAMEDTUPLE:
                return getattr(item, field)
            else:
                raise TypeNotSupportedError

        if mode_list is None:
            target = [item for item in target if keyword in get_attr_with_format(item, field_name, output_format)]
        elif len(mode_list) == 0:
            raise NullFilterConditionError
        else:
            for item in mode_list:
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
        return target
