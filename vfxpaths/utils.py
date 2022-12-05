#!/usr/bin/env python
# -*- encoding: utf-8 -*-
import json

from vfxpaths.global_config import Configuration
from vfxpaths.ability.path_env_resolve import resolve_real_path
from vfxpaths.ability.path_operation import check_file_exists


class RW:
    work_path = Configuration.current_work_path
    target_path = Configuration.current_target_path

    def __init__(self, target_path: str = "", work_path: str = ""):
        if target_path != "":
            self.target_path = target_path

        if work_path:
            self.work_path = work_path

    @property
    def get_target_path(self) -> str:
        return resolve_real_path(self.target_path, None, self.work_path)

    def get_json_data(self, file_path: str = "") -> dict:
        if file_path == "":
            return self.__read_json_file(self.get_target_path)
        else:
            return self.__read_json_file(resolve_real_path(file_path, None, self.work_path))

    def read_file(self, file_path: str = ""):
        pass

    def read_start_file(self, start_str: str):
        pass

    def read_end_file(self, end_str: str):
        pass

    @check_file_exists
    def __read_json_file(self, json_file):
        with open(json_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
        return data

