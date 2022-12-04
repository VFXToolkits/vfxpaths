#!/usr/bin/env python
# -*- encoding: utf-8 -*-
import logging
from copy import copy

from vfxpaths.global_config import Configuration
from vfxpaths.error import NotFound
from vfxpaths.ability.regex_match import MatchModel
from vfxpaths.ability.path_env_resolve import resolve_real_path

log = logging.getLogger(__name__)


class BaseResolve:
    target_path = Configuration.current_target_path
    current_work_path = Configuration.current_work_path
    use_name = ""

    def __init__(self, target_path: str = "",
                 use_name: str = "",
                 current_work_path: str = "",
                 match_model=MatchModel.full
                 ):
        self.match_model = match_model

        if use_name != "":
            if Configuration.config_template.get(use_name):
                self.use_name = use_name
            else:
                msg: str = "use_name: arguments name not exists"
                log.error(msg)
                raise NotFound(msg)

        if target_path != "":
            self.target_path = target_path

        if current_work_path:
            self.current_work_path = resolve_real_path(current_work_path)

        self.__get_target_path = resolve_real_path(self.target_path, None, self.current_work_path)
        self.__get_dict_data: dict = {}
        self.__current_match_target: str = ""
        self.__all_match_target: dict = Configuration.config_template

    @property
    def get_target_path(self) -> str:
        if self.target_path == "":
            log.error("The target path is not set")
            return ""
        return self.__get_target_path

    @staticmethod
    def copy_custom_fields():
        if Configuration.custom_replaced_value:
            new_custom_data = copy(Configuration.custom_replaced_value)
            return new_custom_data
        return


class Resolve(BaseResolve):
    def __init__(self, **key):
        super(Resolve, self).__init__(**key)

        if self.use_name != "":
            self.__current_match_target = Configuration.config_template.get(self.use_name)

    def get_dict_data(self) -> dict:
        if self.__get_target_path == "":
            return self.__get_dict_data

        if self.__current_match_target == "":
            pass

    def __find_match_pattern(self, pattern: str):
        pass
