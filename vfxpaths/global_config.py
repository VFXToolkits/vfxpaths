#!/usr/bin/env python
# -*- encoding: utf-8 -*-

class Base:
    def __getitem__(self, item):
        return getattr(self, item)

    @classmethod
    def config_keys(cls) -> list:
        return [item for item in dir(cls) if not item.startswith("_") and item != "config_keys"]


class VFXPathBaseConfig(Base):

    config_template: dict = {}

    # current run environ root path
    windows_root_path: str = ""
    mac_root_path: str = ""
    linux_root_path: str = ""

    # Custom Value resolves replace
    # If the environment variable does not exist
    # it will be replaced, which means that the priority of the environment variable is high
    custom_replaced_value: dict = {}

    # Configure path by operating system
    custom_root_path: dict = {}

    # Global Path string Replacement Mapping
    global_str_mapping: dict = {}


class TypeRuleFormat(Base):
    # assets assets={"name":{entity_name}_{custom_name}_{version}.{extend}, path="."}
    assets: dict = {}
    shots: dict = {}


class EntityConfig(Base):
    __remove_key = ["config_keys", "rule_format"]

    @classmethod
    def config_keys(cls) -> list:
        return [item for item in dir(cls) if not item.startswith("_") and item in cls.__remove_key]

    entity_name: str = ""
    rule_name: str = ""
    rule_format = TypeRuleFormat
    suffix: str = ""
    prefix: str = ""
    extend: str = ""
    custom_name: str = ""
    category: str = ""
    version: str = "%03d"
    numeral: str = "%04d"
    map_key = {}


class Configuration(VFXPathBaseConfig):
    # The configuration path must be json
    file_path: str = ""
    current_target_path: str = ""
    current_work_path: str = ""
    entity_config = EntityConfig
