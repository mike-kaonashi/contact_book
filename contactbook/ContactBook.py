from contactbook import SCHEMA_PATH, DATA_PATH, OUTPUT_FORMAT, data_helper


def add(*args):
    return data_helper.write_data(args)


def list():
    results = data_helper.read_data(type_=OUTPUT_FORMAT)
    return results


def search(field, param):
    list_ = list()
    return data_helper.filter_data(list_, field,
                                   keyword=param,
                                   mode_list=None)


def age_filter(age=None, age_gt=None, age_gte=None, age_lt=None, age_lte=None):
    mode_list = []
    list_ = list()
    if age:
        mode_list.append({
            'mode': '=',
            'value': age
        })
    if age_gt:
        mode_list.append({
            'mode': '>',
            'value': age_gt
        })
    if age_gte:
        mode_list.append({
            'mode': '>=',
            'value': age_gte
        })
    if age_lte:
        mode_list.append({
            'mode': '<=',
            'value': age_lte
        })
    if age_lt:
        mode_list.append({
            'mode': '<',
            'value': age_lt
        })
    return data_helper.filter_data(list_, 'age',
                                   keyword=None,
                                   mode_list=mode_list)
