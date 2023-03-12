#!/usr/bin/env python
# -*- encoding: utf-8 -*-
# common operation functions of the path
import os
import ctypes
import shutil
from datetime import datetime
import pathlib
import logging
from typing import List

from vfxpaths.ability.path_operation import to_forward_slash, to_resolve_real_path
from vfxpaths.ability.path_env_resolve import resolve_real_path
from vfxpaths.ability.regex_match import RegexCompile
from vfxpaths.ability.path_const import FileMatchModel
from vfxpaths.global_config import Configuration

log = logging.getLogger(__name__)


class SysSpecialFolder:
    def get_temp_path(self):
        if os.name == "nt":
            pass

    @property
    def get_home_path(self) -> str:
        return str(pathlib.Path.home()).replace("\\", "/")


class OperationPath:
    def __init__(self):
        self._target_path = ""
        self._work_path = ""
        self._pathlib_obj = pathlib.Path

    @to_forward_slash
    def change_extension(self, ext: str, file_path: str = "") -> str:
        """
        example: change_extension(c:\folder\file.ma, ".abc")
        return c:\folder\file.abc
        """
        return pathlib.Path(file_path).with_suffix(ext).as_posix()

    @to_forward_slash
    def combine(self, file_name: any, file_path: str = "") -> str:
        """Incoming parameters file_name str or list"""
        return pathlib.Path(file_path, file_name).as_posix()

    @to_resolve_real_path
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

    def create_folders(self, path_list: List[str]) -> List[str]:
        create_results: List[str] = []
        if self._work_path == "":
            raise KeyError("work_path need to set")
        for item in path_list:
            new_dir_path = pathlib.Path(self._work_path)/item
            create_results.append(new_dir_path.as_posix())
            if pathlib.Path.exists(new_dir_path):
                continue
            else:
                new_dir_path.mkdir()
        return create_results

    def glob_target(self, re_model: str) -> List[str]:
        """
        Get all files under the folder
        *.* or **/*.*
        """
        find_path = self._target_path

        if not os.path.exists(self._target_path):
            return []
        if os.path.isfile(find_path):
            find_path = os.path.dirname(self._target_path)
        return [f.as_posix() for f in pathlib.Path(find_path).glob(re_model)]

    def glob_work(self, re_model: str) -> List[str]:
        """
        Get all files under the folder
        *.* or **/*.*
        """
        if not os.path.exists(self._work_path):
            return []
        return [f.as_posix() for f in pathlib.Path(self._work_path).glob(re_model)]

    @to_resolve_real_path
    def create_hidden(self, path: str = "") -> str:
        if pathlib.Path(path).exists():
            return ""
        if not os.path.basename(path).startswith("."):
            return ""
        if os.name == 'nt':
            pathlib.Path(path).mkdir()
            ctypes.windll.kernel32.SetFileAttributesW(path, 0x02)
        else:
            pathlib.Path(path).mkdir()

    @to_forward_slash
    def rename(self, new_name: str, path: str) -> bool:
        if not pathlib.Path(path).exists():
            return False
        pathlib.Path(path).rename(new_name)
        return True

    @to_resolve_real_path
    def del_directory(self, path: str):
        """
        Delete the folder. The folder must be empty
        """
        if pathlib.Path(path).exists():
            pathlib.Path.rmdir(pathlib.Path(path))

    @to_resolve_real_path
    def del_tree(self, path: str):
        if pathlib.Path(path).exists():
            shutil.rmtree(path)

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

    @to_forward_slash
    def extended_suffix_name(self, name: str, path: str = "") -> str:
        file_suffix = pathlib.Path(path).suffix
        if file_suffix:
            log.warning(f"File has no suffix name: {path}")
            return path
        file_name = pathlib.Path(path).stem
        return f"{os.path.dirname(path)}/{file_name}{name}{file_suffix}"

    @to_forward_slash
    def path_match(self, re_model: str, path: str) -> bool:
        return pathlib.PurePath(path).match(re_model)


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

    @property
    def find_first_folder(self) -> str:
        if self.isdir and self.exists:
            all_file_list = os.listdir(self.get_full_path)
            if all_file_list:
                for item in all_file_list:
                    if os.path.isdir("{}/{}".format(self.get_full_path, item)):
                        return "{}/{}".format(self.get_full_path, item)
        return ""

    @property
    def find_first_file(self):
        if self.isdir and self.exists:
            all_file_list = os.listdir(self.get_full_path)
            if all_file_list:
                for item in all_file_list:
                    if os.path.isfile("{}/{}".format(self.get_full_path, item)):
                        return "{}/{}".format(self.get_full_path, item)
        return ""

    @property
    def get_invalid_chars(self) -> bool:
        re_group = RegexCompile.invalid_path.value.match(self.get_full_path)
        if re_group:
            if self.get_full_path.replace(re_group.group(), "") == "":
                return False
            else:
                return True
        return True

    @property
    def get_files(self) -> List[str]:
        if self.exists and self.isdir:
            return [item for item in os.listdir(self.get_full_path) if os.path.isfile(f"{self.get_full_path}/{item}")]
        return []

    @property
    def get_folders(self) -> List[str]:
        if self.exists and self.isdir:
            return [item for item in os.listdir(self.get_full_path) if os.path.isdir(f"{self.get_full_path}/{item}")]
        return []

    @property
    def get_all_files(self) -> List[str]:
        if self.exists and self.isdir:
            return [item for item in os.listdir(self.get_full_path)]
        return []

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

    @property
    def is_w_ok(self) -> bool:
        """os.access(, os.W_OK)"""
        return os.access(self._target_path, os.W_OK)

    @property
    def is_frame(self) -> bool:
        match = RegexCompile.seq_path.value.match(self._target_path)
        if match:
            return True
        return False

    def frame_mark(self, file_name: str = "") -> List:
        if not file_name:
            file_name = self._target_path

        match = RegexCompile.sequence_mark.value.match(file_name)
        if match:
            return [match.group(1), match.group(2), match.group(3), match.group(4)]
        return []

    def is_udim(self, file_name: str = "") -> bool:
        if not file_name:
            file_name = self._target_path
        match = RegexCompile.udim_path.value.match(file_name)
        if match:
            if 1000 <= match.group(1) <= 1099:
                return True
            return False
        return False


class Path(GetAttributePath):
    def __init__(self, target_path: str = "", work_path: str = ""):
        super(Path, self).__init__()

        if target_path == "":
            self._target_path = resolve_real_path(Configuration.current_target_path)
        else:
            self._target_path = target_path

        if self._target_path == "":
            raise KeyError("target_path is none")
        self._target_path = resolve_real_path(self._target_path)

        if work_path == "":
            self._work_path = resolve_real_path(Configuration.current_work_path)
        else:
            self._work_path = resolve_real_path(work_path)

    def udim_list(self, file_name: str) -> List[str]:
        if "<UDIM>" not in file_name:
            return []
        file_suffix = file_name.split("<UDIM>")[0]
        file_prefix = file_name.split("<UDIM>")[1]
        all_file_name = self.glob_target("{}*{}".format(file_suffix, file_prefix))
        udim_file_list = []
        for item_file_name in all_file_name:
            if self.is_udim(os.path.basename(item_file_name)):
                udim_file_list.append(item_file_name)
        return udim_file_list

    def frame_count(self, file_name: str) -> int:
        return len(self.frame_list(file_name))

    def frame_list(self, file_name: str) -> List[str]:
        current_frame_mark = self.frame_mark(file_name)
        if current_frame_mark:
            if FileMatchModel.style2.value in file_name:
                file_prefix = file_name.split(current_frame_mark[0])[0]
                file_suffix = file_name.split(current_frame_mark[0])[1]
            elif FileMatchModel.style3.value in file_name:
                file_prefix = file_name.split(current_frame_mark[2])[0]
                file_suffix = file_name.split(current_frame_mark[2])[1]
            elif FileMatchModel.style1.value in file_name:
                file_prefix = file_name.split(current_frame_mark[3])[0]
                file_suffix = file_name.split(current_frame_mark[3])[1]
            else:
                return []
            return self.glob_target("{}*{}".format(file_prefix, file_suffix))
        else:
            return []

    def frame_format(self):
        pass

    def get_file_version_list(self, suffix: str = "") -> List[str]:
        """
        example: suffix=v*/*.hip
        """
        valid_files: List[str] = []
        if suffix:
            all_file = self.glob_target(suffix)
        else:
            all_file = self.glob_target("*.*")
        for item in all_file:
            file_name = os.path.basename(item)
            match = RegexCompile.file_version_num.value.match(file_name)
            if match:
                valid_files.append(item.replace(f"{self._target_path}/", ""))
        return valid_files

    def get_folder_version_list(self, suffix: str = "") -> List[str]:
        """
        example: suffix=v*/test.hip
        """
        valid_files: List[str] = []
        if suffix:
            all_file = self.glob_target(suffix)
        else:
            all_file = self.glob_target("*.*")
        for item in all_file:
            match = RegexCompile.file_version_num.value.match(os.path.dirname(item))
            if match:
                valid_files.append(item)
        return valid_files

    def get_upversion(self) -> str:
        """
        return max version + 1 path
        """
        if self.isfile:
            match = RegexCompile.file_version_num.value.match(self.get_file_name)
            if match:
                temp_version_file = self.get_file_name.replace(match.groups()[0], "*")
                all_version_count = len(self.glob_target(temp_version_file))
                new_version_file = temp_version_file.replace("*", f"{all_version_count + 1}".zfill(len(match.groups()[0])))
                return f"{self.get_directory}/{new_version_file}"
            else:
                match_dir = RegexCompile.file_version_num.value.match(self.get_directory)
                if not match_dir:
                    return ""
                index = 1
                while True:
                    new_version_path = self._target_path.replace(match_dir.groups()[0], str(index).zfill(len(match_dir.groups()[0])))
                    if not os.path.exists(new_version_path):
                        return new_version_path
                    index += 1

        elif self.isdir:
            match = RegexCompile.file_version_num.value.match(self._target_path)
            index = 1
            while True:
                new_version_path = self._target_path.replace(match.groups()[0], str(index).zfill(len(match.groups()[0])))
                if not os.path.exists(new_version_path):
                    return new_version_path
                index += 1
        else:
            return ""

