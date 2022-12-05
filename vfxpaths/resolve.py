#!/usr/bin/env python
# -*- encoding: utf-8 -*-
import logging
from copy import copy
import re
import functools
from collections import defaultdict

from vfxpaths.global_config import Configuration
from vfxpaths.error import NotFound, FormatError
from vfxpaths.ability.regex_match import MatchModel, RegexCompile
from vfxpaths.ability.path_env_resolve import resolve_real_path

log = logging.getLogger(__name__)


class BaseResolve:
    target_path = Configuration.current_target_path
    current_work_path = Configuration.current_work_path
    use_name = ""

    def __init__(self, target_path: str = "",
                 use_name: str = "",
                 current_work_path: str = "",
                 match_model=MatchModel.center
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

        self._get_target_path = resolve_real_path(self.target_path, None, self.current_work_path)
        self._get_dict_data: dict = {}
        self._current_match_target: str = ""
        self._all_match_target: dict = Configuration.config_template

    @property
    def get_target_path(self) -> str:
        if self.target_path == "":
            log.error("The target path is not set")
            return ""
        return self._get_target_path

    @staticmethod
    def copy_custom_fields():
        if Configuration.custom_replaced_value:
            new_custom_data = copy(Configuration.custom_replaced_value)
            return new_custom_data
        return

    @staticmethod
    def _replace_field(match, field_count):
        field = match.group('stand_in')
        field_count[field] += 1
        field += '{0:02d}'.format(field_count[field])
        expression = match.group('expression')
        if expression is None:
            expression = RegexCompile.str_path_split.value
        return r'(?P<{}>{})'.format(field, expression)


class Resolve(BaseResolve):
    def __init__(self, **key):
        super(Resolve, self).__init__(**key)
        self.__init_use_template()

    @property
    def get_match_target(self) -> str:
        return self._current_match_target

    @property
    def get_all_match_target(self) -> dict:
        return self._all_match_target

    @property
    def get_fields_only_list(self) -> list:
        if self._current_match_target == "":
            return []
        all_field = RegexCompile.field_match.value.findall(self._current_match_target)
        return list(set(all_field))

    @property
    def get_all_fields_only_list(self) -> list:
        if self._current_match_target == "":
            return []
        all_field = RegexCompile.field_match.value.findall(self._current_match_target)
        return all_field

    @property
    def get_value_only_list(self) -> list:
        if self._current_match_target == "":
            return []
        return list(self.get_dict_data.values())

    @property
    def get_dict_data(self) -> dict:
        if self._get_target_path == "":
            log.error("The target path is empty")
            return self._get_dict_data

        if self._current_match_target == "":
            for key, value in self._all_match_target:
                path_dict = self.__find_match_pattern(value)
                if path_dict:
                    return path_dict
        else:
            return self.__find_match_pattern(self._current_match_target)

    def dict_to_path(self, dict_data: dict) -> str:
        if not dict_data:
            return ""
        self.__init_use_template()

        if self._current_match_target == "":
            log.warning("Match_target is none")
            return ""
        full_path = RegexCompile.field_match.value.sub(functools.partial(self.__to_expression_value, data=dict_data),
                                                       self._current_match_target)
        if full_path:
            return full_path.replace("\\.", "/")
        return ""

    @staticmethod
    def __to_expression_value(func_match, data) -> str:
        placeholder = func_match.group(1)
        key_list = placeholder.split('.')

        for item in key_list:
            if not data.get(item):
                msg = 'format data error {0} Missing key parameters {1}.'.format(data, placeholder)
                log.error(msg)
                raise FormatError(msg)
            else:
                return data.get(item)

    def __init_use_template(self):
        if self.use_name != "":
            current_pattern = Configuration.config_template.get(self.use_name)
            if current_pattern:
                self._current_match_target = current_pattern.replace("\\", "/").replace(".", r"\.")
        else:
            log.warning("No template specified for use.")

    def __find_match_pattern(self, pattern: str) -> dict:
        match_expression = self.__convert_full_expression(pattern)
        result = match_expression.search(self._get_target_path)
        if not result:
            log.error("No mapping information was obtained")
            return {}
        result_data: dict = {}
        for key, value in result.groupdict().items():
            new_key: str = key[:-2]
            result_data[new_key] = value
        return result_data

    def __convert_full_expression(self, pattern: str):
        log.info("pattern: {}".format(pattern))
        expression = re.sub(r'{(?P<stand_in>.+?)(:(?P<expression>(\\}|.)+?))?}',
                            functools.partial(self._replace_field, field_count=defaultdict(int)),
                            pattern)
        expression = self.__select_model(expression)
        return re.compile(expression)

    def __select_model(self, expression):
        if self.match_model is MatchModel.stat:
            return "^{}".format(expression)
        elif self.match_model is MatchModel.end:
            return "{}$".format(expression)
        elif self.match_model is MatchModel.full:
            return "^{}$".format(expression)
        return expression
