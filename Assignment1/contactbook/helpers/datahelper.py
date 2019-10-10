import json
import datetime
import collections
from enum import Enum


class TypeEnum(Enum):
    DICTIONARY = 0
    NAMEDTUPLE = 1


class DataHelper:
    """

    """
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
            except FileExistsError:
                raise FileExistsError
            except FileNotFoundError:
                raise FileNotFoundError

    @property
    def _headers(self):
        return [item['name'].lower() for item in self._schema['fields']]

    def read_data(self, type_=TypeEnum.DICTIONARY):
        """Read data from target file and parse to python readable data
        :return:
        """
        try:
            source_ = open(self._data_source, 'r')
        except FileExistsError:
            raise FileExistsError
        except FileNotFoundError:
            raise FileNotFoundError
        results = json.load(source_)
        if type_ is TypeEnum.DICTIONARY:
            # Nothing change
            pass
        elif type_ is TypeEnum.NAMEDTUPLE:
            Object = collections.namedtuple('Object', self._headers)
            results = [Object._make(item.values()) for item in results]

        return results

    def write_data(self, target):
        ...

    def apply_schema(self, target_unit):
        """
        Apply data schema for target obj (only for flatten data)
        :param target_unit:
        :return:
        """
        def cast_dict(unit, prop_name, prop_value, prop_type, metadata=None):
            if prop_type == "string":
                unit[prop_name] = str(prop_value)
            elif prop_type == "integer":
                unit[prop_name] = int(prop_value)
                print(unit)
            elif prop_type == "float":
                unit[prop_name] = float(prop_value)
            elif prop_type == "date":
                date_format = metadata['date_format']
                unit[prop_name] = datetime.datetime.strptime(prop_value, date_format)

        def cast_tuple(unit, prop_name, prop_value, prop_type,metadata=None):
            if prop_type == "string":
                unit._replace(**{prop_name: str(prop_value)})
            elif prop_type == "integer":
                unit._replace(**{prop_name: int(prop_value)})
                print(unit)
            elif prop_type == "float":
                unit._replace(**{prop_name: float(prop_value)})
            elif prop_type == "date":
                date_format = metadata['date_format']
                unit._replace(**{prop_name: datetime.datetime.strptime(prop_value, date_format)})

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
                    cast_tuple(unit, current_name, current_value, current_type, field_props['metadata'])

            except ValueError:
                raise ValueError
        for field in self._schema['fields']:
            cast_type(field, target_unit)
