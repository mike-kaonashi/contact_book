from utils.settings import config
from helpers.datahelper import JsonHelper, TypeEnum

DATA_PATH = config['data']['file_path']
SCHEMA_PATH = config['data']['schema_path']


def add(*args):
    print(args[0])

def list():
    helper = JsonHelper(source=DATA_PATH, schema=SCHEMA_PATH)
    results = helper.read_data(type_=TypeEnum.NAMEDTUPLE)
    for item in results:
        helper.apply_schema(item)
    return results



def search(field=None, param=""):
    ...


def age_filter(age=None, age_gt=None, age_gte=None, age_lte=None):
    ...


a = list()
print(a)