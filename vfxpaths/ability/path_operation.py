#!/usr/bin/env python
# -*- encoding: utf-8 -*-
import os
from vfxpaths.error import FileNotExists

# Class Decorator


def check_file_exists(func):
    def wrapper(self, path_str: str):
        if not os.path.exists(path_str):
            raise FileNotExists()
        if not os.path.isfile(path_str):
            raise FileNotExists("The current path is not a file")
        ret = func(self, path_str)
        return ret
    return wrapper
