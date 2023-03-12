#!/usr/bin/env python
# -*- encoding: utf-8 -*-
from vfxpaths.resolve import Resolve
from .entity import Entity
from vfxpaths.utils import RW
from vfxpaths.path import Path
from vfxpaths.ability.regex_match import MatchModel
from vfxpaths.ability.path_env_resolve import get_root_path, get_custom_root_path
from vfxpaths.initialization import (init_pattern_config,
                                     add_config_template,
                                     register_config_file,
                                     register_config,
                                     register_global_str_mapping,
                                     add_global_str_mapping,
                                     maps_config_field,
                                     set_target_path,
                                     remove_config_template)


def init_config():
    # initialization config
    init_pattern_config()


__all__ = ["Resolve",

           "RW",
           "Path",
           "Entity",

           "add_config_template",
           "remove_config_template",
           "register_config_file",
           "register_config",
           "add_global_str_mapping",
           "register_global_str_mapping",
           "maps_config_field",
           "set_target_path",

           "get_custom_root_path",
           "get_root_path",
           "MatchModel"]
