#!/usr/bin/env python
# -*- encoding: utf-8 -*-
import os
import sys

from vfxpaths.ability.regex_match import RegexCompile
from vfxpaths.global_config import Configuration


def get_root_path() -> str:
    platform = sys.platform
    if platform == "win32":
        return resolve_real_path(Configuration.windows_root_path)
    elif platform == "linux":
        return resolve_real_path(Configuration.linux_root_path)
    elif platform == "darwin":
        return resolve_real_path(Configuration.mac_root_path)
    else:
        return ""


def get_custom_root_path(key_name: str) -> str:
    platform = sys.platform
    current_root = Configuration.custom_root_path.get(key_name)
    if not current_root:
        return ""
    current_root_path = current_root.get(system_field_map(platform), "")
    if current_root_path:
        return resolve_real_path(current_root_path)
    return ""


def path_string_replace(source_path: str) -> str:
    platform = sys.platform
    current_sys = system_field_map(platform)
    all_field_data = Configuration.global_str_mapping
    for item in all_field_data:
        source_path = source_path.replace(item, all_field_data[item].get(current_sys))
    return source_path


def system_field_map(key: str):
    sys_name = {"win32": "windows", "linux": "linux", "darwin": "mac"}
    return sys_name[key]


def resolve_real_path(source_path: str, custom_instance=None, instance: str = "") -> str:
    if source_path == "":
        return ""
    source_path = os.path.expandvars(source_path)
    new_path = source_path.replace("\\", "/")

    if "[" in new_path:
        new_path = env_path_replace(new_path)

    if "[" in new_path:
        new_path = keyword_replace(new_path, custom_instance)

    if new_path.startswith("./"):
        new_path = join_full_path(new_path, instance)
    if os.environ.get("VFXPATHS_GLOBAL_REPLACE") == "1":
        new_path = path_string_replace(new_path)

    if new_path.startswith("[root_path]"):
        new_path = new_path.replace("[root_path]", get_root_path())

    if new_path.startswith("[custom_root_path."):
        temp_path_list = new_path.split(".")[1].split("/")
        use_key = temp_path_list[0].replace("]", "")
        if get_custom_root_path(use_key):
            new_path = new_path.replace(temp_path_list[1], get_custom_root_path(use_key))
    return new_path


def get_resolve_template(source: str) -> str:
    if "[custom_root_path." not in source:
        return source
    temp_path_list = source.split(".")[1].split("/")
    use_key = temp_path_list[0].replace("]", "")
    if get_custom_root_path(use_key):
        new_source = source.replace(temp_path_list[1], get_custom_root_path(use_key))
        return new_source
    return source


def env_path_replace(env_path: str) -> str:

    env_key: list = RegexCompile.env_match.value.findall(env_path)
    for item in env_key:
        env_value = os.environ.get(item)
        if isinstance(env_value, str):
            env_path = env_path.replace("[{}]".format(item), env_value).replace("\\", "/")
    return env_path


def keyword_replace(keyword_path: str, custom_instance=None) -> str:
    if custom_instance is None:
        custom_instance = Configuration.custom_replaced_value
    env_key: list = RegexCompile.env_match.value.findall(keyword_path)
    for item in env_key:
        keyword_value = custom_instance.get(item)
        if isinstance(keyword_value, str):
            if "[" in keyword_value:
                key_value = env_path_replace(keyword_value)
                keyword_path = keyword_path.replace("[{}]".format(item), key_value).replace("\\", "/")

    return keyword_path


def join_full_path(relative_path: str, instance: str = "") -> str:
    if instance == "":
        instance = Configuration.current_work_path

    full_path = os.path.join(instance, relative_path.replace("./", "/"))
    return full_path.replace("\\", "/")
