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


def resolve_real_path(source_path: str, custom_instance=None, instance: str = "") -> str:
    if source_path == "":
        return ""

    new_path = source_path.replace("\\", "/")

    if "[" in new_path:
        new_path = env_path_replace(new_path)

    if "[" in new_path:
        new_path = keyword_replace(new_path, custom_instance)

    if new_path.startswith("./"):
        new_path = join_full_path(new_path, instance)
    return new_path


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
