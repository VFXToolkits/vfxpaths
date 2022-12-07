#!/usr/bin/env python
# -*- encoding: utf-8 -*-
from vfxpaths.resolve import Resolve
from vfxpaths.utils import RW
from vfxpaths.ability.regex_match import MatchModel
from vfxpaths.initialization import (init_pattern_config,
                                     add_config_template,
                                     register_config_file,
                                     register_config,
                                     remove_config_template)


def init_config():
    # initialization config
    init_pattern_config()


__all__ = ["Resolve",
           "add_config_template",
           "remove_config_template",
           "register_config_file",
           "register_config",
           "MatchModel"]

