import os
from .utils.settings import config
from .helpers.datahelper import JsonHelper, TypeEnum, ConditionEnum

DATA_PATH = os.path.join(os.path.dirname(__file__), config['data']['file_path'])
SCHEMA_PATH = os.path.join(os.path.dirname(__file__), config['data']['schema_path'])
helper = JsonHelper(source=DATA_PATH, schema=SCHEMA_PATH)


def add(*args):
    return helper.write_data(args)


def list():
    results = helper.read_data(type_=TypeEnum.NAMEDTUPLE)
    for item in results:
        helper.apply_schema(item)
    return results


def search(field=None, param=None):
    list_ = list()
    return helper.filter_data(list_, field, keyword=param, mode_list=None)


def age_filter(age=None, age_gt=None, age_gte=None, age_lt=None, age_lte=None):
    mode_list = []
    list_ = list()
    if age is not None:
        mode_list.append({
            'mode': '=',
            'value': age
        })
    if age_gt is not None:
        mode_list.append({
            'mode': '>',
            'value': age_gt
        })
    if age_gte is not None:
        mode_list.append({
            'mode': '>=',
            'value': age_gte
        })
    if age_lte is not None:
        mode_list.append({
            'mode': '<=',
            'value': age_lte
        })
    if age_lt is not None:
        mode_list.append({
            'mode': '<',
            'value': age_lt
        })
    return helper.filter_data(list_, 'age', keyword=None, mode_list=mode_list)
