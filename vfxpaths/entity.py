#!/usr/bin/env python
# -*- encoding: utf-8 -*-
import os

from .global_config import Configuration
from .ability.path_env_resolve import resolve_real_path
from .ability.regex_match import RegexCompile
from .ability.path_env_resolve import relative_path_resolving


class EntityBase:
    def _rule_map(self, format_value: str, extend: str = "") -> str:
        if extend:
            format_value = format_value.replace("{extend}", extend)

        all_field = RegexCompile.field_match.value.findall(format_value)
        for item in all_field:
            format_value = format_value.replace(item, self.__field_replace(item))
        return format_value

    def _number_length(self, model: str) -> int:
        match = RegexCompile.sequence_mark.value.match(model)
        return int(match.group(2))

    @staticmethod
    def __field_replace(field):
        current_value = getattr(Configuration.entity_config, field, False)
        if current_value:
            return current_value
        map_key_value = Configuration.entity_config.map_key.get(field)
        return map_key_value


class Entity(EntityBase):
    def __init__(self, work_path: str = "", rule_format: str = ""):

        if work_path == "":
            self._work_path = resolve_real_path(Configuration.current_work_path)
        else:
            self._work_path = resolve_real_path(work_path)

        self.rule_format = rule_format

    @staticmethod
    def rule_config() -> Configuration.entity_config:
        return Configuration.entity_config

    def get_name(self) -> str:
        if not self.rule_format:
            return ""
        current_rule_format: dict = getattr(Configuration.entity_config.rule_format, self.rule_format, "")
        if current_rule_format:
            return self._rule_map(current_rule_format.get("name"))
        return ""

    def get_assets_file_name(self, extend: str = "", version: str = "1", num: str = 1) -> str:
        assets_name = self._rule_map(Configuration.entity_config.rule_format.assets.get("name"), extend)
        version_format = Configuration.entity_config.version
        num_format = Configuration.entity_config.numeral
        if version_format in assets_name:
            version_name = "v{}".format(str(version).zfill(self._number_length(version_format)))
            assets_name = version_name.replace(version_name, version_name)
        if num_format in assets_name:
            assets_name = assets_name.replace(num_format, str(num).zfill(self._number_length(num_format)))
        return assets_name

    def get_custom_name(self, rule_name: str = "") -> str:
        if not rule_name:
            return self.get_name()
        current_rule_format: dict = getattr(Configuration.entity_config.rule_format, rule_name, "")
        if current_rule_format:
            return self._rule_map(current_rule_format.get("name"))
        return ""

    def full_path(self, rule_name: str = "") -> str:
        assets_name = self.get_custom_name(rule_name)
        if not assets_name:
            return ""
        relative_path: str = getattr(Configuration.entity_config.rule_format, rule_name, "").get("path")

        if relative_path:
            if relative_path.startswith("../"):
                new_path = relative_path_resolving(self._work_path, relative_path)
                relative_path = relative_path.replace("../", "")
                return os.path.join(new_path, relative_path, assets_name).replace("\\", "/")
            return os.path.join(self._work_path, relative_path, assets_name).replace("\\", "/")
        else:
            return f"{self._work_path}/{assets_name}"

    def get_all_path(self) -> dict:
        path_data = {}
        for item in Configuration.entity_config.rule_format.config_keys():
            path_data[item] = self.full_path(item)
        return path_data

