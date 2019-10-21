from enum import Enum
from contactbook.helpers import get_attr_with_format, casters
from datetime import datetime


class TypeEnum(Enum):
    STRING = 'string'
    INTEGER = 'integer'
    FLOAT = 'float'
    DOUBLE = 'double'
    DATE = 'date'


class Metadata:
    def __init__(self, metadata):
        self.metadata = metadata

    @property
    def _min(self):
        if 'min' in self.metadata.keys():
            return float(self.metadata['min'])
        return None

    @property
    def _max(self):
        if 'max' in self.metadata.keys():
            return float(self.metadata['max'])
        return None

    @property
    def _format(self):
        if 'format' in self.metadata.keys():
            return self.metadata['format']
        return None

    def get_format(self):
        return self._format

    def is_fit(self, value):
        if self._max and self._min:
            return self._min <= value <= self._max
        elif self._max:
            return value <= self._max
        elif self._min:
            return self._min <= value
        elif self._format:
            try:
                datetime.strptime(value, self._format)
            except ValueError:
                return False
        return True


class Validator(object):

    @staticmethod
    def check_obj_by_schema(obj, schema):
        fields = schema['fields']
        for field in fields:
            type_ = field['type'].lower()
            name = field['name'].lower()
            nullable = field['nullable']
            metadata = Metadata(field['metadata'])
            value = get_attr_with_format(obj, name)
            if (len(str(value)) == 0 or value is None) and nullable is False:
                return False

            if not isinstance(value, casters[type_]) or not metadata.is_fit(casters[type_](value)):
                return False
        return True
