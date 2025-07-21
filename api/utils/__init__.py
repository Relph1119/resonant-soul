#!/usr/bin/env python
# encoding: utf-8
"""
@author: Datawhale
@file: __init__.py.py
@time: 2025/7/21 19:24
@project: resonant-soul
@desc: 
"""
import copy
import os

from api.constants import SERVICE_CONF
from api.utils import file_utils


def conf_realpath(conf_name):
    conf_path = f"conf/{conf_name}"
    return os.path.join(file_utils.get_project_base_directory(), conf_path)


def read_config(conf_name=SERVICE_CONF):
    local_config = {}

    global_config_path = conf_realpath(conf_name)
    global_config = file_utils.load_yaml_conf(global_config_path)

    if not isinstance(global_config, dict):
        raise ValueError(f'Invalid config file: "{global_config_path}".')

    global_config.update(local_config)
    return global_config


CONFIGS = read_config()


def show_configs():
    msg = f"Current configs, from {conf_realpath(SERVICE_CONF)}:"
    for k, v in CONFIGS.items():
        if isinstance(v, dict):
            if "api_key" in v:
                v = copy.deepcopy(v)
                v["api_key"] = "*" * 8
            if "password" in v:
                v = copy.deepcopy(v)
                v["password"] = "*" * 8
            if "access_key" in v:
                v = copy.deepcopy(v)
                v["access_key"] = "*" * 8
            if "secret_key" in v:
                v = copy.deepcopy(v)
                v["secret_key"] = "*" * 8
        msg += f"\n\t{k}: {v}"
    print(msg)


def get_base_config(key, default=None):
    if key is None:
        return None
    if default is None:
        default = os.environ.get(key.upper())
    return CONFIGS.get(key, default)
