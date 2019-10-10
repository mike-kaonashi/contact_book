import yaml
import os

config = None
_static_path = 'config/app-config.yml'
_config_path = os.path.join(os.path.dirname(__file__), _static_path)
try:
    _yml_file = open(_config_path, "r")
    config = yaml.load(_yml_file, Loader=yaml.FullLoader)
except FileNotFoundError:
    raise FileNotFoundError
except FileExistsError:
    raise FileExistsError
