#!/usr/bin/env python
# -*- encoding: utf-8 -*-
from vfxpaths.initialization import init_pattern_config
from vfxpaths.resolve import Resolve


# initialization config

def init_config():
    init_pattern_config()


__all__ = ["Resolve"]

