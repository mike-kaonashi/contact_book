from utils.settings import config
from helpers.datahelper import JsonHelper, TypeEnum

DATA_PATH = config['data']['file_path']
SCHEMA_PATH = config['data']['schema_path']
helper = JsonHelper(source=DATA_PATH, schema=SCHEMA_PATH)

def add(*args):
    helper.write_data(args)

def list():
    results = helper.read_data(type_=TypeEnum.NAMEDTUPLE)
    for item in results:
        helper.apply_schema(item)
    return results



def search(field=None, param=""):
    ...


def age_filter(age=None, age_gt=None, age_gte=None, age_lte=None):
    ...


add('Kiet', '0728495827', 'VNG', 'Bui Vien', 24)
print(list())
# print(a[0])