import yaml

__obj_config__ = None


def __get_configuration_object():
    global __obj_config__
    if __obj_config__ is None:
        with open("config.yml", 'r') as ymlfile:
            __obj_config__ = yaml.load(ymlfile)
    return __obj_config__


def get_value_from_configuration(key):
    if '.' in key:
        return __get_configuration_object()[key.split('.')[0]][key.split('.')[1]]
    return __get_configuration_object()[key]
