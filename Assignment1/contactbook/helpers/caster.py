import os
import sys
import time
import logging
from datetime import datetime
from validator import Validator


_now = datetime.now()
_today = datetime(_now.year, _now.month, _now.day)
_log_file = '{today}_record.log'.format(today=int(time.mktime(_today.timetuple())))
_root_dir = os.path.join(os.path.dirname(sys.modules['__main__'].__file__), 'logs')
_log_path = os.path.join(_root_dir, _log_file)
if not os.path.exists(_root_dir):
    os.makedirs(_root_dir)
logging.basicConfig(filename=_log_path, filemode='a+', level=logging.INFO,
                    format='%(asctime)s-%(levelname)s %(filename)s:%(lineno)s  %(message)s')


class Caster(object):

    def __init__(self, metadata=None):
        self.casters = {
            'string': str,
            'integer': int,
            'float': float,
            'date': lambda value: datetime.strptime(value, metadata.get('date_format'))
        }
        self._metadata = metadata

    def get_metadata(self): 
        return self._metadata 
      
    # setter method 
    def set_metadata(self, value): 
        self._metadata = value

    def cast_dict(self, unit, prop_name, prop_value, prop_type):
        """Cast properties of the dictionary unit fit the schema
        """
        unit[prop_name] = self.casters[prop_type](prop_value) if prop_type in self.casters else None

    def cast_tuple(self, unit, prop_name, prop_value, prop_type):
        """Cast properties of the namedtuple unit fit the schema
        """
        unit = unit._replace(**{prop_name: self.casters[prop_type](prop_value) if prop_type in self.casters else None})
        return unit

    def cast_type(self, field_props, unit):
        validator = Validator()
        current_value = validator.get_attr_with_format(unit, field_props['name'].lower())
        try:
            current_type = field_props['type']
            current_name = field_props['name'].lower()
            if isinstance(unit, dict):
                self.cast_dict(unit, current_name, current_value, current_type)
            elif isinstance(unit, tuple):
                unit = self.cast_tuple(unit, current_name, current_value, current_type)
        except ValueError:
            msg = 'Undefined type of the property'
            logging.error(msg)
            raise ValueError(msg)
        return unit