from enum import Enum


class TypeEnum(Enum):
    STRING = 'string'
    INTEGER = 'integer'
    FLOAT = 'float'
    DOUBLE = 'double'
    DATE = 'date'


class Validator(object):

    @staticmethod
    def get_attr_with_format(item, field):
        if type(item) is dict:
            rs = item[field]
        else:
            rs = getattr(item, field)
        return rs

    def check_obj_by_schema(self, obj, schema):
        fields = schema['fields']
        for field in fields:
            type_ = field['type'].lower()
            name = field['name'].lower()
            nullable = field['nullable']
            metadata = field['metadata']
            value = self.get_attr_with_format(obj, name)
            if len(str(value)) == 0 and nullable is False:
                return False
            if type_ == TypeEnum.STRING.value:
                if not isinstance(value, str):
                    return False
                if 'min' in metadata.keys():
                    if len(value) < int(metadata['min']):
                        return False
                if 'max' in metadata.keys():
                    if len(value) > int(metadata['max']):
                        return False
            elif type_ == TypeEnum.INTEGER.value:
                if not isinstance(value, int):
                    return False
                if 'min' in metadata.keys():
                    if int(value) < int(metadata['min']):
                        return False
                if 'max' in metadata.keys():
                    if int(value) > int(metadata['max']):
                        return False
            elif type_ == TypeEnum.DOUBLE.value or type_ == TypeEnum.FLOAT.value:
                if not isinstance(value, float):
                    return False
                if 'min' in metadata.keys():
                    if float(value) < float(metadata['min']):
                        return False
                if 'max' in metadata.keys():
                    if float(value) > float(metadata['max']):
                        return False
        return True
