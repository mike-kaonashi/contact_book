from datetime import date


casters = {
    'string': str,
    'integer': int,
    'float': float,
    'double': float,
    'date': date
}


def get_attr_with_format(item, field):
    if type(item) is dict:
        rs = item[field]
    else:
        rs = getattr(item, field)
    return rs
