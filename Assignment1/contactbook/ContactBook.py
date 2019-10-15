import os
from contactbook import SCHEMA_PATH, DATA_PATH, OUTPUT_FORMAT, helper


def add(*args):
    return helper.write_data(args)


def list():
    results = helper.read_data(type_=OUTPUT_FORMAT)
    return results


def search(field=None, param=None):
    list_ = list()
    return helper.filter_data(list_, field,
                              keyword=param,
                              mode_list=None,
                              output_format=OUTPUT_FORMAT)


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
    return helper.filter_data(list_, 'age',
                              keyword=None,
                              mode_list=mode_list,
                              output_format=OUTPUT_FORMAT)


# print(add('Mai', '0283918293', 'KMS', 'HN', 24))
# print(list())
# print(search('name', 'i'))
# print(age_filter(age=23))
