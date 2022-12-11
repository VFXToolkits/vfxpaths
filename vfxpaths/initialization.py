#!/usr/bin/env python
# -*- encoding: utf-8 -*-
import os
import json
import logging

from vfxpaths.global_config import Configuration, VFXPathBaseConfig
from vfxpaths.ability.path_env_resolve import resolve_real_path

log = logging.getLogger("vfxpaths.initialization")


def init_pattern_config():
    """Initialise with config file"""
    config_path = os.environ.get("VFXPATHS_CONFIG_FILE")
    if config_path:
        Configuration.file_path = config_path
        load_config_file()
    else:
        find_global_config = globals()
        for item in find_global_config.keys():
            if item.startswith("VFX_paths_config"):
                maps_config_field(find_global_config[item])
                return


def set_target_path(path: str) -> None:
    Configuration.current_target_path = path.replace("\\", "/")


def maps_config_field(config_obj):
    for field in VFXPathBaseConfig.config_keys():
        current_value = getattr(config_obj, field, False)
        if current_value:
            setattr(Configuration, field, current_value)


def register_config_file(config_path: str = ""):
    if config_path == "":
        if Configuration.file_path == "":
            info: str = "config_path parameter cannot be empty"
            log.error(info)
            assert False, info
        else:
            load_config_file()
    else:
        Configuration.file_path = config_path
        load_config_file()


def register_config(pattern_data: dict):
    for field in VFXPathBaseConfig.config_keys():
        if pattern_data.get(field):
            setattr(Configuration, field, pattern_data.get(field))


def add_config_template(key: str, value: str):
    VFXPathBaseConfig.config_template[key] = value


def add_global_str_mapping(key: str, value: dict):
    VFXPathBaseConfig.global_str_mapping[key] = value


def register_global_str_mapping(global_value: dict):
    VFXPathBaseConfig.global_str_mapping = global_value


def remove_config_template(key: str):
    if VFXPathBaseConfig.config_template.get(key):
        del VFXPathBaseConfig.config_template[key]


def cancel_all_config():
    pass


def cancel_config(field: str):
    """
    Clear the configuration of the specified field
    """
    pass


def load_config_file():
    config_data: dict = {}
    config_path = resolve_real_path(Configuration.file_path)
    if config_path.startswith("http"):
        # Get the configuration information through the network get method
        pass
    elif config_path.endswith(".json"):
        if not os.path.exists(config_path):
            log.error("config_path not exists")
            return
        with open(config_path, 'r') as json_file:
            config_data = json.load(json_file)
    else:
        log.error("config file read error")
        return

    register_config(config_data)


__all__ = ["init_pattern_config",
           "register_config_file",
           "register_config",
           "add_config_template",
           "register_global_str_mapping",
           "add_global_str_mapping",
           "remove_config_template",
           "maps_config_field",
           "set_target_path",
           "cancel_all_config"]
