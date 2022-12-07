#!/usr/bin/env python
# -*- encoding: utf-8 -*-


class VFXPathBaseConfig:
    def __getitem__(self, item):
        return getattr(self, item)

    @classmethod
    def config_keys(cls) -> list:
        return [item for item in dir(cls) if not item.startswith("_") and item != "config_keys"]

    config_template: dict = {}

    # current run environ root path
    windows_root_path: str = ""
    mac_root_path: str = ""
    linux_root_path: str = ""

    # Custom Value resolves replace
    # If the environment variable does not exist
    # it will be replaced, which means that the priority of the environment variable is high
    custom_replaced_value: dict = {}


class Configuration(VFXPathBaseConfig):
    # The configuration path must be json
    file_path: str = ""
    current_target_path: str = ""
    current_work_path: str = ""

