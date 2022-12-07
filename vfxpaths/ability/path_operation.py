#!/usr/bin/env python
# -*- encoding: utf-8 -*-
import os

from vfxpaths.error import FileNotExists
from vfxpaths.ability.path_env_resolve import resolve_real_path

# Class Decorator


def check_file_exists(func):
    def wrapper(self, path_str: str = ""):
        if not os.path.exists(path_str):
            raise FileNotExists()
        if not os.path.isfile(path_str):
            raise FileNotExists("The current path is not a file")
        ret = func(self, path_str)
        return ret
    return wrapper


def find_end_file(func):
    def wrapper(self, end_str, path_str: str = ""):
        path_str = get_path_directory(self, path_str)
        get_file_list = [file for file in os.listdir(path_str) if file.endswith(end_str)]

        if not get_file_list:
            raise FileNotExists("The specified file was not found")
        path_str = "{}/{}".format(path_str, get_file_list[0])
        ret = func(self, end_str, path_str)
        return ret
    return wrapper


def find_start_file(func):
    def wrapper(self, data, start_str, path_str: str = ""):
        path_str = get_path_directory(self, path_str)
        get_file_list = [file for file in os.listdir(path_str) if file.startswith(start_str)]

        if not get_file_list:
            raise FileNotExists("The specified file was not found")
        path_str = "{}/{}".format(path_str, get_file_list[0])
        ret = func(self, data, start_str, path_str)
        return ret
    return wrapper


def no_creation_exists(func):
    def wrapper(self, content, path_str: str, model: str = "w", auto_creation: int = 1):
        path_str = get_resolve_real_path(self, path_str)
        if auto_creation:
            file_directory = os.path.dirname(path_str)
            if not os.path.exists(file_directory):
                os.makedirs(file_directory)
        ret = func(self, content, path_str, model, auto_creation)
        return ret
    return wrapper


def get_path_directory(self, path_str: str, no_check: int = 0) -> str:
    path_str = get_resolve_real_path(self, path_str)
    if os.path.isfile(path_str):
        path_str = os.path.dirname(path_str)

    if no_check:
        return path_str
    if not os.path.exists(path_str):
        raise FileNotExists()
    return path_str


def get_resolve_real_path(self, path_str: str) -> str:
    if path_str == "":
        path_str = self.get_target_path
    else:
        path_str = resolve_real_path(path_str, None, self.work_path)
    return path_str
