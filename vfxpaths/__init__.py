#!/usr/bin/env python
# -*- encoding: utf-8 -*-
from vfxpaths.resolve import Resolve
from vfxpaths.utils import RW
from vfxpaths.ability.regex_match import MatchModel
from vfxpaths.ability.path_env_resolve import get_root_path, get_custom_root_path
from vfxpaths.initialization import (init_pattern_config,
                                     add_config_template,
                                     register_config_file,
                                     register_config,
                                     register_global_str_mapping,
                                     add_global_str_mapping,
                                     maps_config_field,
                                     remove_config_template)


def init_config():
    # initialization config
    init_pattern_config()


__all__ = ["Resolve",

           "add_config_template",
           "remove_config_template",
           "register_config_file",
           "register_config",
           "add_global_str_mapping",
           "register_global_str_mapping",
           "maps_config_field",

           "get_custom_root_path",
           "get_root_path",
           "MatchModel"]

