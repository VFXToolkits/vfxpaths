#!/usr/bin/env python
# -*- encoding: utf-8 -*-
# common operation functions of the path
import os
from datetime import datetime
import pathlib
import logging

from vfxpaths.ability.path_operation import to_forward_slash
from vfxpaths.ability.path_env_resolve import resolve_real_path
from vfxpaths.global_config import Configuration

log = logging.getLogger(__name__)


class SysSpecialFolder:
    def get_temp_path(self):
        pass

    @property
    def get_home_path(self) -> str:
        return str(pathlib.Path.home()).replace("\\", "/")


class OperationPath:
    def __init__(self):
        self._target_path = ""
        self._pathlib_obj = pathlib.Path

    @to_forward_slash
    def change_extension(self, ext: str, file_path: str = "") -> str:
        """
        example: change_extension(c:\folder\file.ma, ".abc")
        return c:\folder\file.abc
        """
        return str(pathlib.Path(file_path).with_suffix(ext)).replace("\\", "/")

    @to_forward_slash
    def combine(self, file_name: any, file_path: str = "") -> str:
        """Incoming parameters file_name str or list"""
        return str(pathlib.Path(file_path, file_name)).replace("\\", "/")

    @to_forward_slash
    def create_folder(self, path: str = "") -> bool:
        current_path = pathlib.Path(path)
        if current_path.is_file():
            log.error("The current path is a file")
            return False
        if current_path.exists():
            log.warning("The current directory already exists")
            return False
        pathlib.Path.mkdir(current_path)
        return True

    def create_folders(self, path: list):
        pass

    def create_hidden(self, path: str = ""):
        pass

    def rename(self, new_name: str):
        pass

    def del_directory(self, path: str):
        """
        Delete the folder. The folder must be empty
        """
        pass

    @to_forward_slash
    def fallback_dir(self, hierarchy: int = 0, path: str = "") -> str:

        path_list = path.split("/")
        if len(path_list) <= hierarchy:
            hierarchy = len(path_list) - 1

        index = len(path_list) - hierarchy

        return "/".join(path_list[0:index])

    @to_forward_slash
    def header_directory(self, hierarchy: int = 1, path: str = ""):
        path_list = path.split("/")
        if len(path_list) <= hierarchy:
            hierarchy = len(path_list)

        path_list = path.split("/")[0: hierarchy]
        return "/".join(path_list)


class GetAttributePath(OperationPath):

    @property
    def get_paths(self) -> list:
        return self._target_path.split("/")

    @property
    def get_directory(self) -> str:
        if self.isdir:
            return self._target_path
        return os.path.dirname(self._target_path)

    @property
    def get_file_name(self) -> str:
        return self._pathlib_obj(self._target_path).name

    @property
    def get_file_without_extension(self) -> str:
        return self._pathlib_obj(self._target_path).stem

    @property
    def get_extension(self) -> str:
        return self._pathlib_obj(self._target_path).suffix

    @property
    def get_without_extension(self) -> str:
        if self.get_extension == "":
            return self._target_path
        return self._target_path.replace(self.get_extension, "")

    @property
    def get_root(self) -> str:
        return self._pathlib_obj(self._target_path).root

    @property
    def get_full_path(self) -> str:
        return self._target_path

    def find_first_folder(self):
        pass

    def find_first_file(self):
        pass

    def get_invalid_chars(self):
        pass

    @property
    def exists(self):
        return self._pathlib_obj(self._target_path).exists()

    @property
    def isfile(self) -> bool:
        return self._pathlib_obj(self._target_path).is_file()

    @property
    def isdir(self) -> bool:
        return self._pathlib_obj(self._target_path).is_dir()

    @property
    def getatime(self) -> str:
        st_atime = self._pathlib_obj(self._target_path).stat().st_atime
        return datetime.fromtimestamp(st_atime).strftime("%Y-%m-%d %H:%M:%S")

    @property
    def getctime(self) -> str:
        """
        File creation time
        """
        st_ctime = self._pathlib_obj(self._target_path).stat().st_ctime
        return datetime.fromtimestamp(st_ctime).strftime("%Y-%m-%d %H:%M:%S")

    @property
    def getmtime(self) -> str:
        """Last modified file time"""
        st_mtime = self._pathlib_obj(self._target_path).stat().st_mtime
        return datetime.fromtimestamp(st_mtime).strftime("%Y-%m-%d %H:%M:%S")

    @property
    def getsize(self) -> float:
        """
        Folder Get all file sizes, unit mb
        """
        total_size = 0.0
        path_obj = self._pathlib_obj(self._target_path)

        if not path_obj.exists():
            return 0.0

        if path_obj.is_file():
            return path_obj.stat().st_size / 1024 * 1024

        for dirpath, dirnames, filenames in os.walk(self._target_path):
            for f in filenames:
                fp = os.path.join(dirpath, f)
                # skip if it is symbolic link
                if not os.path.islink(fp):
                    total_size += os.path.getsize(fp)

        return total_size / 1024 * 1024

    def is_w_ok(self) -> bool:
        """os.access(, os.W_OK)"""
        return os.access(self._target_path, os.W_OK)


class Path(GetAttributePath):
    def __init__(self, target_path: str = ""):
        super(Path, self).__init__()
        self.work_path = ""

        if target_path == "":
            self._target_path = Configuration.current_target_path
        else:
            self._target_path = target_path

        if self._target_path == "":
            raise KeyError("target_path is none")
        self._target_path = resolve_real_path(self._target_path)
