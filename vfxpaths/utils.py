#!/usr/bin/env python
# -*- encoding: utf-8 -*-
import json
import os.path

from vfxpaths.global_config import Configuration
from vfxpaths.ability.path_env_resolve import resolve_real_path
from vfxpaths.ability.path_operation import check_file_exists, find_end_file, find_start_file, no_creation_exists


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

    @no_creation_exists
    def write_json(self, data: dict, file_path: str = "", model: str = "w", auto_creation: int = 1):
        if isinstance(data, dict):
            raise TypeError("data parameter must be dict")
        if model == "w":
            self.__write_json_file(file_path, data)
        else:
            if os.path.exists(file_path):
                old_data: dict = self.__read_json_file(file_path)
                old_data.update(data)
                self.__write_json_file(file_path, old_data)

    def read_file(self, file_path: str = ""):
        if file_path == "":
            return self.__read_file(self.get_target_path)
        else:
            return self.__read_file(resolve_real_path(file_path, None, self.work_path))

    @no_creation_exists
    def write_file(self, content, file_path: str = "", model: str = "w", auto_creation: int = 1):
        if isinstance(content, list):
            self.__write_file("\n".join(content), file_path, model)
            return
        self.__write_file(content, file_path, model)

    @find_start_file
    def read_start_file(self, start_str: str, file_path: str = ""):
        return self.__read_file(file_path)

    @find_end_file
    def read_end_file(self, end_str: str, file_path: str = ""):
        return self.__read_file(file_path)

    @find_start_file
    def read_start_json(self, end_str: str, file_path: str = ""):
        return self.__read_json_file(file_path)

    @find_end_file
    def read_end_json(self, end_str: str, file_path: str = ""):
        return self.__read_json_file(file_path)

    @check_file_exists
    def __read_json_file(self, json_file: str) -> dict:
        if not json_file.endswith(".json"):
            return {}
        with open(json_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
        return data

    @staticmethod
    def __write_json_file(json_file: str, data: dict):
        if not json_file.endswith(".json"):
            raise TypeError("The file must be json")
        with open(json_file, 'w', encoding="utf-8") as f:
            json.dump(data, f, indent=4, ensure_ascii=False)

    @check_file_exists
    def __read_file(self, file_path) -> str:
        with open(file_path, "r", encoding="utf-8") as f:
            text = f.read()
        return text

    @staticmethod
    def __write_file(content: str, file_path: str, model: str):
        with open(file_path, model, encoding="utf-8") as f:
            f.write(content)

